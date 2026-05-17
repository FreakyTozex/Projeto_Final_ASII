from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'O que está a pensar?',
                'class': 'form-control',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'content': 'Publicação',
            'image': 'Imagem (opcional)',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Escreva um comentário...',
                'class': 'form-control comment-input',
                'autocomplete': 'off',
            }),
        }
        labels = {
            'content': '',
        }
