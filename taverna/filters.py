from django_filters import FilterSet, ChoiceFilter
from .models import Post, Category, PostReply


class PostFilter(FilterSet):
    cat = ChoiceFilter(field_name='category__category', choices=Category.THEMES, label='Поиск по категории')
    class Meta:
        model = Post
        fields = ('title', 'post_rating', 'author')

class Post2Filter(FilterSet):
    class Meta:
        model = PostReply
        fields = ('post__title', 'post__time_in')