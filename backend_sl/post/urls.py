from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [

    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('post_detail/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_review/<slug:slug>/', views.PostReview.as_view(), name='post_review'),
    path('create_star/', views.StarView.as_view(), name='create_star'),

    ]