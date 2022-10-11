from django.shortcuts import render
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView)
from rest_framework.generics import (ListAPIView, ListCreateAPIView)
from .models import Post, Comment, Star
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer, StarCreateSerializer, PostCreateSerializer, CommentCreateSerializer
from account.models import UserAccount
from django.db.models import Q

# Create your views here.

# for create post you should send the data and the user_id
# used for create
class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostCreateSerializer


# for the post owner for update and delete and show
# used for edit and delete
class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    lookup_field = 'slug'

    # to allow partial update (patch)
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# another users who want to see the post - just get method -
# used for show
class PostReview(RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    lookup_field = 'slug'


class StarCreateView(CreateAPIView):
    queryset = Star.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StarCreateSerializer


class CommentCreateView(CreateAPIView):
    queryset = Star.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CommentCreateSerializer


class PostListView(ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()

        name = self.request.query_params.get('filter')
        if name is not None:
            queryset = queryset.filter(Q(title=name) | Q(description=name)
                                       | Q(title__contains=name) | Q(description__contains=name)
                                       | Q(file__contains=name))

        posts_owner_slug = self.request.query_params.get('posts_owner_slug')
        if posts_owner_slug is not None:
            queryset = queryset.filter(Q(user__profile__slug=posts_owner_slug))

        return queryset