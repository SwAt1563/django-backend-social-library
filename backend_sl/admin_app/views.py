from django.shortcuts import render
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from post.serializers import PostSerializer
from post.models import Post
from django.db.models import Q
from account.models import UserAccount
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from notification.models import Notification
from rest_framework.decorators import api_view, permission_classes

# Create your views here.


class PostListView(ListAPIView):

    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()

        name = self.request.query_params.get('filter')
        if name is not None:
            queryset = queryset.filter(Q(title=name) | Q(description=name)
                                       | Q(title__contains=name) | Q(description__contains=name)
                                       | Q(file__contains=name) | Q(user__username__contains=name)
                                       | Q(user__first_name__contains=name) | Q(user__last_name__contains=name)
                                       | Q(user__email=name) | Q(status=name))


        return queryset


class RemovePostView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def destroy(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id', 0)
            post_slug = request.data.get('post_slug', '')
            user_id = UserAccount.objects.filter(pk=user_id).first()
            post = Post.objects.filter(slug=post_slug).first()
            if post:
                post_owner = post.user
                post_title = post.title
            if post and user_id and user_id.is_admin:
                self.perform_destroy(post)
                sender = user_id
                receiver = post_owner
                content = f'{sender.get_full_name} removed your post: {post_title}'
                Notification.objects.create(from_user=sender, to_user=receiver, content=content)
            else:
                raise Http404
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([])
def accept_post(request):
    if request.method == 'POST':
        data = request.data
        user_id = data.get('user_id', 0)
        post_slug = data.get('post_slug', '')
        user_id = UserAccount.objects.filter(pk=user_id).first()
        post = Post.objects.filter(slug=post_slug).first()
        if post:
            post_owner = post.user
            post_title = post.title
        if post and user_id and user_id.is_admin:
            post.status = Post.Status.COMPLETED
            post.save()
            sender = user_id
            receiver = post_owner
            content = f'{sender.get_full_name} accepted your post: {post_title}'
            Notification.objects.create(from_user=sender, to_user=receiver, content=content)
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)