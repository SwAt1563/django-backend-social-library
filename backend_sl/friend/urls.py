from django.urls import path
from friend import views

app_name = 'friend'

urlpatterns = [
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('unfollow/', views.UnFollowView.as_view(), name='unfollow'),
    path('following/', views.FollowingListView.as_view(), name='following'),
    path('followers/', views.FollowersListView.as_view(), name='followers'),
    ]


