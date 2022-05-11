from django.contrib import admin
from .models import BlogPost, PostComment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('author', 'date_created', 'title', 'post')

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'date_created', 'blog_post', 'comment')

admin.site.register(BlogPost, BlogAdmin)
admin.site.register(PostComment, PostCommentAdmin)


