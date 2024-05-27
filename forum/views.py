from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count
from django.contrib import messages
from .models import Post
from .forms import CommentForm, PostForm

def post_list(request):
    """
    View for all the posts
    """
    queryset = Post.objects.filter(status=1).annotate(comment_count=Count('comments')).order_by('-created_on')
    paginator = Paginator(queryset, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    context = {
            'page_obj': page_obj,
            'posts': page_obj.object_list,
            'is_paginated': is_paginated,
        }

    return render(request, "forum/index.html", context)

def post_create(request):
    """
    Create a post view
    """

    post_form = PostForm() 


    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(
                request,
                "Thanks for posting! Your post will be visible shortly."
            )
            return redirect('home')
    
    
    return render(
        request, 
        "forum/post_create.html",
        {
            'post_form': post_form,
        },
    )
    

def post_detail(request, slug):
    """
    Display an individual post
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.count()
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

    comment_form = CommentForm()

    return render(
        request,
        "forum/post_detail.html",
        {"post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        },

    )