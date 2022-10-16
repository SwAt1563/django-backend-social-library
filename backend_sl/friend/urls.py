from django.urls import path
from friend import views

app_name = 'friend'


urlpatterns = [
    # you should send the user_id for user who want to make follow/unfollow request
    # and the user_slug for the user who want to make follow/unfollow to him
    # the data should be in body request

    # POST METHOD: user_id, following_user_slug
    path('follow/', views.FollowView.as_view(), name='follow'),
    # DELETE METHOD: user_id, following_user_slug
    path('unfollow/', views.UnFollowView.as_view(), name='unfollow'),



    # you should send the user_id for user who want to show the data
    # and the user_slug for the profile which you want to see the following/followers people on it
    # send data by GET METHOD 'parameters'

    # GET METHOD PARAMETERS: related_user_slug, user_id, filter (OPTIMAL)
    # RESULT: following people profiles
    path('following/', views.FollowingListView.as_view(), name='following'),

    # GET METHOD PARAMETERS: related_user_slug, user_id, filter (OPTIMAL)
    # RESULT: followers people profiles
    path('followers/', views.FollowersListView.as_view(), name='followers'),
    ]


