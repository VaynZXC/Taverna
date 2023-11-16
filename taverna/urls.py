from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from taverna.views import Hub, PostDetail, PostCreate, ProfileView

app_name = 'taverna'
urlpatterns = [
    path('', Hub.as_view(), name='Hub'),
    path('news/<int:pk>', (PostDetail.as_view()), name='news_detail'),
    path('news/create', PostCreate.as_view(), name='news_create'),
    path('account/profile', ProfileView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)