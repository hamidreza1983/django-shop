from django import forms
from .models import *


class ProductReplayForm(forms.ModelForm):
    class Meta:
        model = ProductReplay
        fields = ['text']


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['text']
