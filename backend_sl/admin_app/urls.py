from django.urls import path
from admin_app import views

app_name = 'admin_app'

urlpatterns = [

    # you should send the search parameter with GET METHOD
    # or you will get all posts
    # GET METHOD: filter (OPTIMAL PARAMETER)
    path('dashboard/', views.PostListView.as_view(), name='dashboard'),

    # you should send the user_id of admin and post_slug of the deleted post
    # DELETE METHOD: user_id, post_slug
    path('remove_post/', views.RemovePostView.as_view(), name='remove_post'),

    # you should send the user_id of admin and post_slug of the accepted post
    # POST METHOD: user_id, post_slug
    path('accept_post/', views.accept_post, name='accept_post'),

    ]


