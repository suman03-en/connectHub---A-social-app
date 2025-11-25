from django import forms 
from .models import Post,Comment

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","description","image"]

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]