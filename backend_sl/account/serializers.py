from rest_framework import serializers

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, get_user_model
)
from .models import UserAccount, validate_email
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from user_profile.models import Profile


class UsernameTokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        self.user = UserAccount.objects.filter(username=attrs[self.username_field]).first()

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')

        if not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

        if not self.user.is_admin:
            raise ValidationError('The user not admin')

        data = {}

        refresh = self.get_token(self.user)

        # we can return more data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['username'] = str(self.user.username)
        data['email'] = str(self.user.email)
        data['user_id'] = self.user.id
        data['is_admin'] = self.user.is_admin
        if hasattr(self.user, 'profile'):
            data['profile_slug'] = str(self.user.profile.slug)

        return data


class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = get_user_model().EMAIL_FIELD

    def validate(self, attrs):
        self.user = UserAccount.objects.filter(email=attrs[self.username_field]).first()

        if not self.user:
            raise ValidationError('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise ValidationError('Incorrect credentials.')

        if not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

        data = {}

        refresh = self.get_token(self.user)

        # we can return more data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['username'] = str(self.user.username)
        data['email'] = str(self.user.email)
        data['user_id'] = self.user.id
        data['is_admin'] = self.user.is_admin
        if hasattr(self.user, 'profile'):
            data['profile_slug'] = str(self.user.profile.slug)

        return data


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True,
                                     validators=[UniqueValidator(queryset=UserAccount.objects.all())])
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=UserAccount.objects.all()), validate_email])

    password = serializers.CharField(required=True, write_only=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)
    question = serializers.CharField(max_length=200, required=True)
    answer = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'password', 'password2', 'question',
                  'answer')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password2': 'password fields not match'}
            )
        return attrs

    def create(self, validated_data):
        user = UserAccount.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            question=validated_data['question'],
            answer=validated_data['answer'],
        )
        user.set_password(validated_data['password'])
        user.save()
        # create related profile for this user
        Profile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email')
        read_only_fields = ('email',)
