from .models import Comment, Post, Category
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
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Categories'
    )


    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Add a title',
            }),
            'content': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Add text',
                'style': 'height: 200px;',
            }),
        }
        labels = {
            'title': '',
            'content': '',
        }