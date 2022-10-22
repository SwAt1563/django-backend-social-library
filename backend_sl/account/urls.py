from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import check_token_expired, EmailTokenObtainPairView, RegisterUserAPIView, UsernameTokenObtainPairView, check_email_and_answer, change_password

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

        # for know if the token expired or not
        # POST METHOD: access, refresh
        # RESULT: (access, 200) if updated or not expired, (403) finish refresh expired
        path('check_token/', check_token_expired, name='check_token_expired'),

        # POST METHOD: username, email, password, password2, question, answer
        path('register/', RegisterUserAPIView.as_view(), name='register'),

        # POST METHOD: email, question, answer
        # Result: reset_password_token
        path('reset_password_token/', check_email_and_answer, name='reset_password_token'),

        # POST METHOD: new_password (validation password), reset_password_token
        path('change_password/', change_password, name='change_password'),



    ]


