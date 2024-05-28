from . import views
from django.urls import path

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post/', views.post_create, name='post_create'),
    path('top/', views.top_posts, name='top_posts'),
    path('<slug:slug>/', views.post_detail, name = 'post_detail'),
]