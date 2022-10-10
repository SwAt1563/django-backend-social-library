from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import ProfileSerializer
from .models import Profile
from rest_framework.permissions import AllowAny
# Create your views here.


class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer
    lookup_field = 'slug'


    # to allow partial update (patch)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)