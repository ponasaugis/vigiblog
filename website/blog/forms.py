from .models import BlogPost, PostComment
from django import forms
from django.contrib.auth.models import User




# Komentaro rašymo forma
class PostReviewForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('comment', 'blog_post', 'reviewer',)
        widgets = {'blog_post': forms.HiddenInput(), 'reviewer': forms.HiddenInput(), 'comment': forms.Textarea(attrs={'class':'md-textarea form-control m-0', 'placeholder':'Enter your comment...', 'rows':'2'})}
        labels = {
            'comment': ''
        }


# Įrašo rašymo forma
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'post']
        widgets = {'title': forms.Textarea(attrs={'class':'md-textarea form-control w-75', 'placeholder':'Enter a Title...', 'rows':'1'})}
        labels = {
            'title': '',
            'post': '',
        }


# Įrašo redagavimo forma
class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'post']
        widgets = {'title': forms.Textarea(
            attrs={'class': 'md-textarea form-control w-75', 'placeholder': 'Enter a Title...', 'rows': '1'})}
        labels = {
            'title': '',
            'post': '',
        }


# Komentaro redagavimo forma
class EditCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['comment']
        widgets= {'comment': forms.Textarea(attrs={'class':'md-textarea form-control w-50', 'rows':'5'})}
        labels = {
            'comment': ''
        }

