from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainSerializer, RegistrationSerializer, UsernameTokenObtainSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer


class UsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = UsernameTokenObtainSerializer

class RegisterUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
