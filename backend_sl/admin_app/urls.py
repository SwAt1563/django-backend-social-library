from django.urls import path
from admin_app import views

app_name = 'admin_app'

urlpatterns = [

    path('dashboard/', views.PostListView.as_view(), name='dashboard'),
    path('remove_post/', views.RemovePostView.as_view(), name='remove_post'),
    path('accept_post/', views.accept_post, name='accept_post'),

    ]


