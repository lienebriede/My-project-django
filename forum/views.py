from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.db.models import Count
from .models import Post
from .forms import CommentForm

class PostList(generic.ListView):
    """
    View for all the posts
    """
    model = Post
    queryset = Post.objects.all()
    template_name = "forum/index.html"
    paginate_by = 5

    """
    These methods access the comment_count
    """
    def get_queryset(self):
        queryset = super().get_queryset().annotate(comment_count=Count('comments'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset()
        return context


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