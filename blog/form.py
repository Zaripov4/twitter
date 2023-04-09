from django import forms
from django.forms import ClearableFileInput

from .models import File, Post


class FeedModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["body"]


class FileModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file"]
        widgets = {
            "file": ClearableFileInput(attrs={"multiple": True}),
        }
