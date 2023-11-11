from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from taverna.views import Hub, PostDetail

app_name = 'taverna'
urlpatterns = [
    path('', Hub.as_view(), name='Hub'),
    path('news/<int:pk>', (PostDetail.as_view()), name='news_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)