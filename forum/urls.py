from . import views
from django.urls import path

urlpatterns = [
    path('', views.post_list, name='home'),
    path('post/', views.post_create, name='post_create'),
    path('top/', views.top_posts, name='top_posts'),
    path('search/', views.search_results, name='search_results'),
    path('<slug:slug>/', views.post_detail, name = 'post_detail'),
    path('category/<int:category_id>/', views.post_list_by_category, name='post_list_by_category'),
]