from django.urls import path

from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('', views.index, name='yt-analyzer-index'), 
    path('search', views.search, name='search')
]