from django.urls import path, include
from . import views

from taverna.views import Hub

app_name = 'taverna'
urlpatterns = [
      path('sign/', include('sign.urls')),
      path('taverna/', Hub.as_view(), name='hub')
]