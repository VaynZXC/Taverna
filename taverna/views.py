from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, TemplateView
from .models import Post, Author, Category, CategorySubscriber, User, UserAvatar, Reply, PostReply
from .filters import PostFilter, Post2Filter
from .forms import PostForm
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
import operator

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


# Create your views here.
class Hub(ListView):
  model = Post
  template_name = 'taverna/hub.html'
  context_object_name = 'HubAllNews'
  posts = Post.objects.filter(news_or_proposal='NE')
  queryset = posts.order_by('-id')
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
    context['form'] = PostForm
    context['current_author'] = self.get_current_author()
    return context
  
  def get_current_author(self):
    if self.request.user.is_anonymous:
        return None
    else:
      author = Author.objects.get(user=self.request.user)
      return author

  def get_queryset(self):
    queryset = super().get_queryset()
    self.filterset = PostFilter(self.request.GET, queryset)
    return self.filterset.qs

  form_class = PostForm

  def post(self, request, *args, **kwargs):
      form = self.form_class(request.POST)
      if form.is_valid():
          obj = form.save(commit=False)
          obj.author = Author.objects.get(user=request.user)
          obj.save()
          form.save_m2m()
      return super().get(request, *args, **kwargs)
  
class PostDetail(DetailView):
    model = Post
    template_name = 'taverna/news_detail.html'
    context_object_name = 'news'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class PostCreate(UserPassesTestMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('taverna.add_post')
    template_name = 'taverna/news_create.html'
    form_class = PostForm
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = request.user

        if form.is_valid():
          obj = form.save(commit=False)
          obj.author = Author.objects.get(user=user)
          obj.save()
          form.save_m2m()
          return redirect('taverna:news_detail', obj.pk)
        else:
          raise PermissionDenied("Форма не валидна")
          
       
    def test_func(self, *args, **kwargs):
        author = Author.objects.get(user=self.request.user.id)
        yesterday = datetime.now() - timedelta(days=1)
        post_day = Post.objects.filter(author=author, time_in__gt=yesterday).count()
        print(post_day)
        if post_day > 2:
            raise PermissionDenied("Допускается постить до 3 новостей в день")
        else:
            return redirect('taverna:profile')
        

@method_decorator(login_required(login_url = '/'), name='dispatch')
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('taverna.change_post')
    template_name = 'taverna/news_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    success_url = reverse_lazy('taverna:Hub')

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('taverna.delete_post')
    model = Post
    template_name = 'taverna/news_delete.html'
    context_object_name = 'news'
    queryset = Post.objects.all()
    success_url = reverse_lazy('taverna:Hub')

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'account/profile.html'
    context_object_name = 'ProfileReplys'
    model = PostReply
    
    def get_replys(self):
      user = self.request.user
      if user.groups.filter(name = 'author').exists():
        author = Author.objects.get(user=self.request.user)
        posts = Post.objects.filter(author=author)
        queryset = PostReply.objects.none()
        for post in posts:
          if PostReply.objects.filter(post=post).exists():
            replys = PostReply.objects.filter(post=post).all()
            #for reply in replys:
            queryset |= replys
      return queryset


    def get_queryset(self):
      queryset = self.get_replys()
      self.filterset = Post2Filter(self.request.GET, queryset)
      return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        categories = CategorySubscriber.objects.filter(subscriber=user.id)
        yesterday = datetime.now() - timedelta(days=1)

        context['is_not_author'] = not user.groups.filter(name = 'author').exists()
        context['is_not_subscriber'] = not user.groups.filter(name='subscriber').exists()

        if user.groups.filter(name = 'author').exists():
          author = Author.objects.get(user=user) 
          context['posts_on_this_day'] = Post.objects.filter(author=author, time_in__gt=yesterday).count()
          context['filter'] = Post2Filter(self.request.GET, queryset=self.get_queryset())

        if categories:
          context['subscribed'] = True
          context['categories'] = categories
        else:
          context['subscribed'] = False
        return context
    

def change_avatar(request):
    return render(request, 'alerts/change_avatar.html')

class ConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'categories/subscribe.html'
    model = Post
    
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(pk=pk)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['subscribed'] = True
            context['category'] = category
        else:
            context['subscribed'] = False
            context['category'] = category
        return context

class ConfirmationViewUnsubscribe(LoginRequiredMixin, TemplateView):
    template_name = 'categories/unsubscribe.html'
    model = Post
    
    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=pk)
        context['category'] = category
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('taverna:profile')

def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user.id)
        email = user.email
        html = render_to_string(
            'mail/subscribe.html',
            {
                'category': category,
                'user': user,    
            },
          )
        
        msg = EmailMultiAlternatives(
              subject = f'{category} subscription',
              body = f'Здравствуй, {user}. Новая статья в твоём любимом разделе!',
              from_email = DEFAULT_FROM_EMAIL,
              to = [email, ],
            )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('taverna:profile')
    return redirect('taverna:hub')
    
def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return redirect('taverna:hub')


class BulletinBoard(ListView):
  model = Post
  template_name = 'bulletin_board/bulletin_board.html'
  context_object_name = 'AllBoardProposal'
  posts = Post.objects.filter(news_or_proposal='PR')
  queryset = posts.order_by('-id')
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
    context['form'] = PostForm
    context['current_author'] = self.get_current_author()
    return context
  
  def get_current_author(self):
    if self.request.user.is_anonymous:
        return None
    else:
      author = Author.objects.get(user=self.request.user)
      return author

  def get_queryset(self):
    queryset = super().get_queryset()
    self.filterset = PostFilter(self.request.GET, queryset)
    return self.filterset.qs

  form_class = PostForm

  def post(self, request, *args, **kwargs):
      form = self.form_class(request.POST)
      if form.is_valid():
          obj = form.save(commit=False)
          obj.author = Author.objects.get(user=request.user)
          obj.save()
          form.save_m2m()
      return super().get(request, *args, **kwargs)
  

@login_required
def reply(request, pk): 
    user = request.user
    post = Post.objects.get(pk=pk)
    reply = Reply.objects.get_or_create(user=user)
    PostReply.objects.create(post=post, reply=reply[0])

    
    email = user.email
    html = render_to_string(
        'mail/reply.html',
        {
            'reply': reply,
            'user': user,    
        },
      )
    
    msg = EmailMultiAlternatives(
          subject = f'Новый отклик на вашь пост',
          body = f'{user} откликнулся на ваше объявление',
          from_email = DEFAULT_FROM_EMAIL,
          to = [email, ],
        )
    msg.attach_alternative(html, 'text/html')

    try:
        msg.send()
    except Exception as e:
        print(e)
    return redirect('taverna:profile')

        
def unreply(request, pk):
    post_reply_obj = PostReply.objects.get(pk=pk)
    post_reply_obj.delete()

    user = post_reply_obj.reply.user

    email = user.email
    html = render_to_string(
        'mail/reply.html',
        {
            'reply': reply,
            'user': user,    
        },
      )
    
    msg = EmailMultiAlternatives(
          subject = f'Ваш отклик отклонили',
          body = f'{user}, ваш отклик отклонили, но вы всегда можете попробовать снова!',
          from_email = DEFAULT_FROM_EMAIL,
          to = [email, ],
        )
    msg.attach_alternative(html, 'text/html')

    try:
        msg.send()
    except Exception as e:
        print(e)
        
    return redirect('taverna:profile')

def reply_accept_notice(request, pk):
    post_reply_obj = PostReply.objects.get(pk=pk)
    post_reply_obj.delete()

    user = post_reply_obj.reply.user
    author = post_reply_obj.post.author.user

    email = user.email
    html = render_to_string(
        'mail/reply.html',
        {
            'reply': reply,
            'user': user,    
        },
      )
    
    msg = EmailMultiAlternatives(
          subject = f'Ваш отклик отклонили',
          body = f'{user}, ваш отклик приняли. Вот почта афтора: {author.email} !',
          from_email = DEFAULT_FROM_EMAIL,
          to = [email, ],
        )
    msg.attach_alternative(html, 'text/html')

    try:
        msg.send()
    except Exception as e:
        print(e)
        
    return redirect('taverna:profile')