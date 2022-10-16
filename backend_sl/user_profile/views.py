from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from .serializers import ProfileSerializer
from .models import Profile
from django.db.models import Q

from rest_framework.settings import api_settings
from .permissions import ProfileOwnerUpdateAllowRetrievePermission, CheckUserPermission


# Create your views here.


class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (*api_settings.DEFAULT_PERMISSION_CLASSES, ProfileOwnerUpdateAllowRetrievePermission)
    serializer_class = ProfileSerializer
    lookup_field = 'slug'

    # to allow partial update (patch)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TopUsersListView(ListAPIView):
    permission_classes = (*api_settings.DEFAULT_PERMISSION_CLASSES, CheckUserPermission)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = sorted(Profile.objects.all(), key=lambda profile: profile.user.get_total_user_stars, reverse=True)[
                   :3]
        return queryset


class UsersListView(ListAPIView):
    permission_classes = (*api_settings.DEFAULT_PERMISSION_CLASSES, CheckUserPermission)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()

        name = self.request.query_params.get('filter')
        if name is not None:
            queryset = queryset.filter(Q(user__first_name=name) | Q(user__last_name=name)
                                       | Q(user__first_name__contains=name) | Q(user__last_name__contains=name)
                                       | Q(user__username__exact=name))

        return queryset
