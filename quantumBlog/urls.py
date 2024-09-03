# QuantumIndex/quantumBlog/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('review/<int:post_id>/create/', views.create_review, name='create_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('about/', views.about, name='about'),
]
