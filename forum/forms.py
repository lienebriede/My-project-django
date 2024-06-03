from .models import Comment, Post, Category
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Add a comment',
                'style': 'height: 80px;',
            }),
        }
        labels = {
            'body': '',
        }

class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Categories'
    )


    class Meta:
        model = Post
        fields = ('title', 'content', 'categories')
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


    # Customizes categories field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].choices = [
            (category.id, category.name) for category in Category.objects.all()
    ]

    