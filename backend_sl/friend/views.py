from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from .models import UserFollowing
from .serializers import FollowCreateSerializer
from user_profile.serializers import ProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from account.models import UserAccount
from user_profile.models import Profile
from django.db.models import Q
from notification.models import Notification
# Create your views here.


class FollowView(CreateAPIView):
    queryset = UserFollowing.objects.all()
    serializer_class = FollowCreateSerializer
    permission_classes = (AllowAny,)

class UnFollowView(DestroyAPIView):
    queryset = UserFollowing.objects.all()
    serializer_class = FollowCreateSerializer
    permission_classes = (AllowAny,)


    def destroy(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id', 0)
            following_user_slug = request.data.get('following_user_slug', '')
            user_id = UserAccount.objects.filter(pk=user_id).first()
            following_user_id = UserAccount.objects.filter(profile__slug=following_user_slug).first()
            instance = UserFollowing.objects.filter(user_id=user_id, following_user_id=following_user_id).first()
            if instance:
                self.perform_destroy(instance)
                sender = user_id
                receiver = following_user_id
                content = f'{sender.get_full_name} unfollow you'
                Notification.objects.create(from_user=sender, to_user=receiver, content=content)
            else:
                raise Http404
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)



# we should send user_slug of the profile
# and the user_id of the user who login the website
class FollowersListView(ListAPIView):

    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = None

        related_user_slug = self.request.query_params.get('related_user_slug')
        if related_user_slug is not None:
            user = UserAccount.objects.filter(profile__slug=related_user_slug).first()
            if user:
                followers = user.followers
                if followers:
                    accounts = followers.values_list('user_id', flat=True)
                    queryset = Profile.objects.all().filter(user__in=accounts)

        return queryset


class FollowingListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = None

        related_user_slug = self.request.query_params.get('related_user_slug')
        if related_user_slug is not None:
            user = UserAccount.objects.filter(profile__slug=related_user_slug).first()
            if user:
                following = user.following
                if following:
                    accounts = following.values_list('following_user_id', flat=True)
                    queryset = Profile.objects.all().filter(user__in=accounts)

        return queryset