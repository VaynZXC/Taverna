from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from taverna.views import Hub, PostDetail, PostCreate, ProfileView, upgrade_me, subscribe, PostDelete
from taverna.views import unsubscribe, ConfirmationViewUnsubscribe, ConfirmationView, PostUpdate, change_avatar

app_name = 'taverna'
urlpatterns = [
    path('', Hub.as_view(), name='Hub'),
    path('news/<int:pk>', (PostDetail.as_view()), name='news_detail'),
    path('news/create', PostCreate.as_view(), name='news_create'),
    path('account/profile', ProfileView.as_view(), name='profile'),
    path('account/upgrade.html', upgrade_me, name='upgrade'),
    path('news/update/<int:pk>', PostUpdate.as_view(),  name='news_update'),
    path('news/delete/<int:pk>', PostDelete.as_view(),  name='news_delete'),

    path('category/<int:pk>', ConfirmationView.as_view(), name='category'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe' ),
    path('category/unsubscribe/<int:pk>', ConfirmationViewUnsubscribe.as_view(), name='category_unsubscribe'),
    path('category/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe' ),

    path('change_avatar/', change_avatar, name='change_avatar'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)