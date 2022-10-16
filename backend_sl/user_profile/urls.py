from django.urls import path
from user_profile import views

app_name = 'user_profile'

urlpatterns = [

        # FOR GET THE PROFILE INFORMATION BY ANY USER
        # OR FOR UPDATE THE PROFILE DATA BY THE PROFILE OWNER
        # URL: user_profile/p/profile_slug
        # GET METHOD PARAMETERS: user_id
        # RESULT: PROFILE OWNER INFO
        # OR
        # PUT METHOD: user_id, (PARAMETERS THAT YOU WANT TO UPDATE - NOT REQUIRE ALL - SAME AS PATCH METHOD)
        # RESULT: PROFILE OWNER INFO
        path('p/<slug:slug>/', views.ProfileView.as_view(), name='profile'),

        # GET THE TOP THREE USERS WHOSE HAVE HIGH STARS
        # GET METHOD PARAMETERS: user_id
        # RESULT: 3 TOP PROFILES
        path('top_users/', views.TopUsersListView.as_view(), name='top_users'),

        # GET ALL PROFILES OR DEPEND ON THE SEARCH PARAMETERS
        # GET METHOD PARAMETERS: user_id, filter (OPTIMAL FOR SEARCH ABOUT SPECIAL PROFILES)
        # RESULT: ALL PROFILES
        path('all_users/', views.UsersListView.as_view(), name='all_users'),
    ]


