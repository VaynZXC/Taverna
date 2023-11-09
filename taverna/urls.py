from django.urls import path, include
from . import views

from taverna.views import Hub

app_name = 'taverna'
urlpatterns = [
      path('', Hub.as_view(), name='Hub')
]