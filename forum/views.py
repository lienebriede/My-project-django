from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Count, Q
from django.contrib import messages
from .models import Post, Like, Category
from .forms import CommentForm, PostForm
from django.template import RequestContext
from django.utils.html import mark_safe
import re

def search_results(request):
    """
    Display posts filtered by search query
    """
    query = request.GET.get('q')
    if query:
        queryset = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query), 
            status=1
        ).annotate(comment_count=Count('comments')).order_by('-created_on')
    
        # Highlight search results
        for post in queryset:
            post.title = mark_safe(re.sub(re.escape(query), f'<span class="highlight">{query}</span>', post.title, flags=re.IGNORECASE))
            post.content = mark_safe(re.sub(re.escape(query), f'<span class="highlight">{query}</span>', post.content, flags=re.IGNORECASE))
    
    else:
        queryset = Post.objects.none() 

    context = {
        'query': query,
        'posts': queryset,
    }

    return render(request, "forum/search_results.html", context)

def post_list(request):
    """
    Display all the posts (latest first)
    """
    query = request.GET.get('q', '')
    queryset = Post.objects.filter(status=1).annotate(comment_count=Count('comments')).order_by('-created_on') 

    paginator = Paginator(queryset, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    context = {
            'page_obj': page_obj,
            'posts': page_obj.object_list,
            'is_paginated': is_paginated,
            'query': query,
        }

    return render(request, "forum/index.html", context)

def top_posts(request):
    """
    Display posts ordered by popularity
    """
    queryset = Post.objects.filter(status=1).annotate(
        comment_count=Count('comments'),
        popularity=Count('likes') + Count('comments')
    ).order_by('-popularity', '-created_on')
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'is_paginated': is_paginated,
    }

    return render(request, "forum/top_posts.html", context)


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
            post_form.save_m2m()
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
    likers = post.likes.all()
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(
                request,
                "Thanks for commenting!"
            )

    comment_form = CommentForm()

    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

        if 'like' in request.POST:
            if is_liked:
                post.likes.filter(user=request.user).delete()
                is_liked = False
            else:
                Like.objects.create(post=post, user=request.user)
                is_liked = True

    return render(
        request,
        "forum/post_detail.html",
        {"post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
        "is_liked": is_liked,
        "likers": likers,
        },

    )

def post_list_by_category(request, category_id):
    """
    Display posts filtered by category
    """
    category = get_object_or_404(Category, id=category_id)
    queryset = Post.objects.filter(status=1, categories=category).annotate(comment_count=Count('comments')).order_by('-created_on')
    
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'is_paginated': is_paginated,
        'selected_category': category.id,
    }

    return render(request, "forum/index.html", context)

def base_view(request):
    """
    Load categories for base template
    """
    categories = Category.objects.all()
    return {'categories': categories}    