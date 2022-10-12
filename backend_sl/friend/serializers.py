from rest_framework import serializers
from .models import UserFollowing
from account.models import UserAccount
from notification.models import Notification


class FollowCreateSerializer(serializers.ModelSerializer):
    following_user_slug = serializers.SlugField(source='following_user_id')

    class Meta:
        model = UserFollowing
        fields = ('user_id', 'following_user_slug')

    def create(self, validated_data):
        following_user_slug = validated_data.pop('following_user_id', '')
        following_user_id = UserAccount.objects.filter(profile__slug=following_user_slug).first()
        validated_data['following_user_id'] = following_user_id

        sender = validated_data.get('user_id')
        receiver = following_user_id
        content = f'{sender.get_full_name} follow you'
        Notification.objects.create(from_user=sender, to_user=receiver, content=content)

        return super().create(validated_data)

