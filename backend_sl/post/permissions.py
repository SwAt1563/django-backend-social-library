from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Post


class CheckUserPermission(BasePermission):
    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)

        if response:
            user, token = response
            if request.method == 'GET':
                user_id = request.GET.get('user_id', 0)
                if str(user.id) == str(user_id):
                    return True
            elif request.method in ('PUT', 'POST', 'DELETE'):
                user_id = request.data.get('user_id', 0)
                if str(user.id) == str(user_id):
                    return True
        return False


class CheckPostOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)

        if response:
            user, token = response
            if request.method in ('PUT', 'DELETE'):
                user_id = request.data.get('user_id', 0)
                if str(user.id) == str(user_id):
                    post_slug = request.resolver_match.kwargs.get('slug')
                    try:
                        get_post = Post.objects.get(user=user, slug=post_slug)
                        return True
                    except Post.DoesNotExist:
                        return False
        return False
