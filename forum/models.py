from django.db import models
from django.contrib.auth.models import User


# Variable for approved posts
STATUS = ((0, "Not Approved"), (1, "Approved"))

class Post(models.Model):
    """
    Model for posts
    """
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
        )
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
        
    # ordered by newest posts first    
    class Meta:
        ordering = ["-created_on"]

    # returns only two first lines of comment text
    def get_content_preview(self):
        return '\n'.join(self.content.split('\n')[:2])

    # converts a string for a title in database
    def __str__(self):
        return f"{self.title} by {self.author}"
