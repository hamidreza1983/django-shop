from django import forms

from .models import Comment, Replay

class ReplayForm(forms.ModelForm):
    class Meta:
        model = Replay
        fields = ['text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']