from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Variable for approved posts
STATUS = ((0, "Not Approved"), (1, "Approved"))

class Category(models.Model):
    """
    Model for categories
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} ID: {self.id}"


class Post(models.Model):
    """
    Model for posts
    """
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
        )
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    categories = models.ManyToManyField(Category, related_name='posts')
        

    # ordered by newest posts first    
    class Meta:
        ordering = ["-created_on"]


    # generates a slug automatically
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        
    # returns only two first lines of comment text
    def get_content_preview(self):
        words = self.content.split()  
        first_25_words = words[:25]  
        return ' '.join(first_25_words)

    # returns a string for admin interface
    def __str__(self):
        return f"{self.title} by {self.author}"

class Comment(models.Model):
    """
    Model for comments
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    # returns a string for admin interface
    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"

class Like(models.Model):
    """
    Model for likes
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # user can like one post only once
    class Meta:
        unique_together = ('post', 'user')

    # returns a string for admin interface
    def __str__(self):
        return f"Liked by {self.post.author} on {self.post.title}"

    