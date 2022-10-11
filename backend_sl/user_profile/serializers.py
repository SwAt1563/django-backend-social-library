from rest_framework import serializers
from .models import Profile
from account.serializers import UserSerializer

# you can update the user fields by send
#$ user.first_name
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user_profile:profile', lookup_field='slug')
    user = UserSerializer()
    user_stars = serializers.SerializerMethodField()
    profile_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('url', 'profile_slug', 'user', 'image', 'age', 'phone', 'address', 'status', 'about_me', 'user_stars')

    # for nested serializer we need this for update the user data
    def update(self, instance, validated_data):
        user, user_data = None, None

        # for send first_name: you should write 'user.first_name'
        if validated_data.get('user'):
            user_data = validated_data.pop('user')
            user = instance.user
        instance = super().update(instance, validated_data)

        if user:
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()
        instance.save()

        return instance

    def get_user_stars(self, profile):
        return profile.user.get_total_user_stars

    def get_profile_slug(self, profile):
        return profile.slug




