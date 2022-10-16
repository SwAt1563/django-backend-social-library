from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainSerializer, RegistrationSerializer, UsernameTokenObtainSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.models import UserAccount
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .permissions import AdminUserPermission





class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer

# just for admins
class UsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = UsernameTokenObtainSerializer
    permission_classes = (AdminUserPermission,)


class RegisterUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer



@api_view(['POST'])
@permission_classes((AllowAny,))
def change_password(request):
    if request.method == 'POST':
        data = request.data
        user_id = data.get('user_id', 0)
        post_slug = data.get('post_slug', '')
        admin = UserAccount.objects.filter(pk=user_id).first()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)