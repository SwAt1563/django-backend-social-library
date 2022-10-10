from rest_framework import serializers
from .models import Profile
from account.serializers import UserSerializer

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user_profile:profile', lookup_field='slug')
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('url', 'user', 'image', 'age', 'phone', 'address', 'status', 'about_me')

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


