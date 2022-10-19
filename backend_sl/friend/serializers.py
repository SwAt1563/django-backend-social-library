from rest_framework import serializers
from .models import UserFollowing
from account.models import UserAccount
from notification.models import Notification
from rest_framework.validators import ValidationError
from django.db import IntegrityError


class FollowCreateSerializer(serializers.ModelSerializer):
    following_user_slug = serializers.SlugField(source='following_user_id')

    class Meta:
        model = UserFollowing
        fields = ('user_id', 'following_user_slug')

    def create(self, validated_data):
        try:
            following_user_slug = validated_data.pop('following_user_id', '')
            following_user = UserAccount.objects.filter(profile__slug=following_user_slug).first()
            validated_data['following_user_id'] = following_user

            # make notification
            sender = validated_data.get('user_id')
            receiver = following_user
            content = f'{sender.get_full_name} follow you'
            Notification.objects.create(from_user=sender, to_user=receiver, content=content)
        except UserAccount.DoesNotExist:
            raise ValidationError('The user not exist')

        try:
            return super().create(validated_data)
        except IntegrityError:  # for handle the unique follow
            raise ValidationError('this follow exists before')



