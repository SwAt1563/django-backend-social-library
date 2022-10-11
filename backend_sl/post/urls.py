from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [

    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_delete/<slug:slug>/', views.PostDetailView.as_view(), name='post_delete'),
    path('post_edit/<slug:slug>/', views.PostDetailView.as_view(), name='post_edit'),
    path('post_review/<slug:slug>/', views.PostReview.as_view(), name='post_review'),
    path('star_create/', views.StarCreateView.as_view(), name='star_create'),
    path('comment_create/', views.CommentCreateView.as_view(), name='comment_create'),

    path('all_posts/', views.PostListView.as_view(), name='all_posts'),
    path('posts_owner/', views.PostListView.as_view(), name='posts_owner'),

    ]