from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, TemplateView
from .models import Post, Author, Category, CategorySubscriber, User
from .filters import PostFilter
from .forms import PostForm
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta


# Create your views here.
class Hub(ListView):
  model = Post
  template_name = 'taverna/hub.html'
  context_object_name = 'HubAllNews'
  queryset = Post.objects.order_by('-id')
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
    context['form'] = PostForm
    return context
  
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
    permission_required = ('news.add_post')
    template_name = 'taverna/news_create.html'
    form_class = PostForm
    
    def post(self, request, *args, **kwargs):
       form = self.form_class(request.POST)
       user = request.user

       if form.is_valid():
          obj = form.save(commit=False)
          obj.author = Author.objects.get(user=user)
          obj.save()
          form.save_m2m()
          return redirect('taverna:news_detail', obj.pk)
       
    def test_func(self, *args, **kwargs):
        author = Author.objects.get(user=self.request.user.id)
        yesterday = datetime.now() - timedelta(days=1)
        post_day = Post.objects.filter(author=author, time_in__gt=yesterday).count()
        print(post_day)
        if post_day > 2:
            raise PermissionDenied("Допускается постить до 3 новостей в день")
        else:
            return redirect('taverna:profile')
        



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        author = Author.objects.get(user=user)
        categories = CategorySubscriber.objects.filter(subscriber=user.id)
        yesterday = datetime.now() - timedelta(days=1)

        context['is_not_author'] = not user.groups.filter(name = 'author').exists()
        # context['is_not_subscriber'] = not user.groups.filter(name='subscriber').exists()
        context['posts_on_this_day'] = Post.objects.filter(author=author, time_in__gt=yesterday).count()

        # if categories:
        #   context['subscribed'] = True
        #   context['categories'] = categories
        # else:
        #   context['subscribed'] = False
        # return context