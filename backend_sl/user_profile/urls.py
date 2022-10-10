from django.urls import path
from user_profile import views

app_name = 'user_profile'

urlpatterns = [
        path('p/<slug:slug>/', views.ProfileView.as_view(), name='profile')
    ]


