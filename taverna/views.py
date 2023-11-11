from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Author, Category, CategorySubscriber, User
from .filters import PostFilter
from .forms import PostForm
from django.core.cache import cache

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