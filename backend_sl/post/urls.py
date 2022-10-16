from django.urls import path
from post import views

app_name = 'post'

urlpatterns = [

    # any user can create post and send the request to the admins wait until accept it to public the post
    # POST METHOD: title, description, file, user_id
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),

    # JUST POST OWNER CAN EDIT OR DELETE BY THESE LINKS
    # URL: post_delete/post_slug
    # DELETE METHOD: user_id
    path('post_delete/<slug:slug>/', views.PostDetailView.as_view(), name='post_delete'),
    # URL: post_edit/post_slug
    # PUT METHOD: user_id
    path('post_edit/<slug:slug>/', views.PostDetailView.as_view(), name='post_edit'),

    # URL: post_review/post_slug
    # GET METHOD: NO PARAMETERS
    path('post_review/<slug:slug>/', views.PostReview.as_view(), name='post_review'),

    # POST METHOD: post_slug, user_id
    path('star_create/', views.StarCreateView.as_view(), name='star_create'),
    # DELETE METHOD: post_slug, user_id
    path('star_remove/', views.StarRemoveView.as_view(), name='star_remove'),

    # POST METHOD PARAMETERS: user_id, post_slug, comment
    path('comment_create/', views.CommentCreateView.as_view(), name='comment_create'),

    # for get all posts and you can filter the posts or get by the posts owner
    # GET METHOD PARAMETERS: posts_owner_slug (OPTIMAL), filter (OPTIMAL)
    path('all_posts/', views.PostListView.as_view(), name='all_posts'),


    ]