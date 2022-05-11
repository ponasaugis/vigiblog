from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse
from ckeditor.fields import RichTextField


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    title = models.TextField('Title', max_length=2000)
    post = RichTextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.author}"


class PostComment(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    blog_post = models.ForeignKey(BlogPost, related_name='comments',on_delete=models.CASCADE, null=True, blank=False)
    comment = models.TextField('Comment', max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post ID: {self.blog_post.id} - {self.comment}"

