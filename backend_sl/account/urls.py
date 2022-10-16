from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import EmailTokenObtainPairView, RegisterUserAPIView, UsernameTokenObtainPairView

app_name = 'account'

urlpatterns = [
        # for admins login by username
        # POST METHOD: username, password
        # RESULT: refresh, access, username, email, user_id, profile_slug
        path('token/', UsernameTokenObtainPairView.as_view(), name='token_obtain_pair'),
        # for normal users login by email
        # POST METHOD: email, password
        # RESULT: refresh, access, username, email, user_id, profile_slug
        path('token_by_email/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair_by_email'),

        # for update the access token you should send refresh token in POST METHOD
        # POST METHOD: refresh
        # RESULT: access
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

        # POST METHOD: username, email, password, password2, question, answer
        path('register/', RegisterUserAPIView.as_view(), name='register'),
    ]


