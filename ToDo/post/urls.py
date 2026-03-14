from django.urls import path
from .views import PostListView, PostDetailView, CommentListView

urlpatterns = [
    path('',       PostListView.as_view(),   name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/',     CommentListView.as_view(),name='comment-list'),
]