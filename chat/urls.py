from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('repos/<str:repo>/',repo_view,name="repo_view"),
    path('chat',chat_view,name="chat"),
]