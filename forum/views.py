from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Post

class PostList(generic.ListView):
    """
    View for all the posts
    """
    queryset = Post.objects.all()
    template_name = "post_list.html"

