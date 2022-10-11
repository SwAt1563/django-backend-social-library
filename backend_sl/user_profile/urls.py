from django.urls import path
from user_profile import views

app_name = 'user_profile'

urlpatterns = [
        path('p/<slug:slug>/', views.ProfileView.as_view(), name='profile'),
        path('top_users/', views.TopUsersListView.as_view(), name='top_users'),
        path('all_users/', views.UsersListView.as_view(), name='all_users'),
    ]


