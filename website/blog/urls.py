
from django.urls import path, include

from . import views
from .views import Posts, PostDetail, CreatePost, CreateView, PostComment, UpdatePost, DeletePost, UserPosts, delete_comment, UpdateComment

urlpatterns = [
    path('', Posts.as_view(), name='index'),
    path('post/<int:pk>', PostDetail.as_view(), name='post'),
    path('tinymce/', include('tinymce.urls')),
    path('register/', views.register, name='register'),
    path('post/create', CreatePost.as_view(), name='post-create'),
    path('post/<int:pk>/update', UpdatePost.as_view(), name='post-update'),
    path('post/<int:pk>/delete', DeletePost.as_view(), name='post-delete'),
    path('post/', UserPosts.as_view(), name='user-posts'),
    path('post/<int:pk>/delete-comment', views.delete_comment, name='delete-comment'),
    path('post/<int:pk>/update-comment', UpdateComment.as_view(), name='comment-update'),


]