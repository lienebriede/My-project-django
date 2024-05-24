from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Leave a Comment',
            }),
        }
        labels = {
            'body': '',
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        