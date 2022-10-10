from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import EmailTokenObtainPairView, RegisterUserAPIView, UsernameTokenObtainPairView

app_name = 'account'

urlpatterns = [
        # for admins login by username
        path('token/', UsernameTokenObtainPairView.as_view(), name='token_obtain_pair'),
        # for normal users login by email
        path('token_by_email/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair_by_email'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('register/', RegisterUserAPIView.as_view(), name='register'),
    ]


