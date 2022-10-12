from rest_framework import serializers
from .models import Profile
from account.serializers import UserSerializer
from account.models import UserAccount
from friend.models import UserFollowing
from notification.models import Notification
from rest_framework.response import Response

# you can update the user fields by send
# user.first_name
# we should send user_id of the user who login the website to know the relation between the enter user and him
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user_profile:profile', lookup_field='slug')
    user = UserSerializer()
    user_stars = serializers.SerializerMethodField(read_only=True)
    profile_slug = serializers.SerializerMethodField(read_only=True)
    is_friend = serializers.SerializerMethodField(read_only=True, default=False)
    relation_date = serializers.SerializerMethodField(read_only=True, default=None)
    number_of_followers = serializers.SerializerMethodField(read_only=True, default=0)
    number_of_following = serializers.SerializerMethodField(read_only=True, default=0)
    number_of_posts = serializers.SerializerMethodField(read_only=True, default=0)
    notifications = serializers.SerializerMethodField(read_only=True, default=None)


    class Meta:
        model = Profile
        fields = ('url', 'profile_slug', 'user', 'image', 'age', 'phone', 'address', 'status', 'about_me', 'user_stars',
                  'is_friend', 'relation_date', 'number_of_followers', 'number_of_following', 'number_of_posts', 'notifications')

    # we should send user_id as parameter to GET method to know if this user is friend to him or not
    def get_is_friend(self, profile):
        data = self.context['request'].GET
        if data:
            if data.get('user_id'):
                current_user = UserAccount.objects.filter(pk=data.get('user_id')).first()
                enter_user = profile.user
                try:
                    relation = UserFollowing.objects.get(user_id=current_user, following_user_id=enter_user)
                    return True
                except UserFollowing.DoesNotExist:
                    relation = None
        return False

    # just get the notification if the current user same as the enter user
    def get_notifications(self, profile):
        data = self.context['request'].GET
        if data:
            if data.get('user_id'):
                user_id = data.get('user_id')
                current_user = UserAccount.objects.filter(pk=user_id).first()
                enter_user = profile.user
                if current_user == enter_user:
                    notifications = current_user.my_received_notifications
                    senders = notifications.values('from_user__username', 'from_user__profile__slug',
                                                   'from_user__profile', 'content')
                    senders = list(senders)

                    for i in range(len(senders)):
                        username = senders[i].pop('from_user__username')
                        profile_slug = senders[i].pop('from_user__profile__slug')
                        profile_id = senders[i].pop('from_user__profile')
                        image = Profile.objects.get(pk=profile_id).image
                        content = senders[i].pop('content')
                        if image:
                            request = self.context.get('request')
                            image_url = image.url
                            image = request.build_absolute_uri(image_url)
                        else:
                            image = None

                        senders[i] = {
                            'username': username,
                            'profile_slug': profile_slug,
                            'image': image,
                            'content': content,
                        }


                    return senders
        return None

    def get_relation_date(self, profile):
        data = self.context['request'].GET
        if data:
            if data.get('user_id'):
                user_id = data.get('user_id')
                current_user = UserAccount.objects.filter(pk=user_id).first()
                enter_user = profile.user
                try:
                    relation = UserFollowing.objects.get(user_id=current_user, following_user_id=enter_user)
                    return relation.created
                except UserFollowing.DoesNotExist:
                    relation = None
        return None


    def get_number_of_followers(self, profile):
        return profile.user.get_total_followers

    def get_number_of_following(self, profile):
        return profile.user.get_total_following

    def get_number_of_posts(self, profile):
        return profile.user.get_total_posts


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




