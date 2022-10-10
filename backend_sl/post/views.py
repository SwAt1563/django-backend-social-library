from django.shortcuts import render
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView)
from rest_framework.generics import (ListAPIView, ListCreateAPIView)
from .models import Post, Comment, Star
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer, StarSerializer
# Create your views here.

# for create post you should send the data and the user_id
class CreatePostView(CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer



# for the post owner for update and delete and show
class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    lookup_field = 'slug'


    # to allow partial update (patch)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# another users who want to see the post - just get method -
class PostReview(RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    lookup_field = 'slug'


class StarView(CreateAPIView):
    queryset = Star.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StarSerializer
    lookup_field = 'slug'



