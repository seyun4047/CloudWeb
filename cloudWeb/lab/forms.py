from django import forms
from .models import Post, QRPost

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image']

# class PostForm2(forms.ModelForm):
#     image = forms.ImageField(label="Choose Image")
#     content = forms.CharField(label="data", widget=forms.Textarea)
#
#     class Meta:
#         model = QRPost
#         fields = ("image", "content")