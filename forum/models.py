from django.db import models
from django.contrib.auth.models import User


# Variable for approved posts
STATUS = ((0, "Not Approved"), (1, "Approved"))

class Post(models.Model):
    """
    Model for posts
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
        )
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.author} on {self.created_on}"
