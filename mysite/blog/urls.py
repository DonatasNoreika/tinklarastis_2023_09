from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('usercomments/', views.UserCommentListView.as_view(), name='usercomments'),
    path('userposts/', views.UserPostListView.as_view(), name='userposts'),
    path('', views.PostListView.as_view(), name="posts"),
    path('<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('posts/new/', views.PostCreateView.as_view(), name="post_new"),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name="post_delete"),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name="post_update"),
    path('posts/<int:post_id>/commentdelete/<int:pk>/', views.CommentDeleteView.as_view(), name="comment_delete"),
    path('posts/<int:post_id>/commentedit/<int:pk>/', views.CommentUpdateView.as_view(), name="comment_edit"),
    path('posts/usercommentdelete/<int:pk>/', views.UserCommentDeleteView.as_view(), name="usercomment_delete"),
    path('posts/usercommentedit/<int:pk>/', views.UserCommentUpdateView.as_view(), name="usercomment_edit"),
    path('profile/', views.profile, name='profile'),
]
