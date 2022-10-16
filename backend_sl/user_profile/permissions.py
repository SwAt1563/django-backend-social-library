from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Profile


class ProfileOwnerUpdateAllowRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        def check_profile_owner(user):
            profile_slug = request.resolver_match.kwargs.get('slug')
            try:
                get_profile = Profile.objects.get(user=user, slug=profile_slug)
                return True
            except Profile.DoesNotExist:
                return False

        response = JWTAuthentication().authenticate(request)
        if response:
            user, token = response
            if request.method == 'GET':
                user_id = request.GET.get('user_id', 0)
                if str(user.id) == str(user_id):
                    return True

            elif request.method == 'PUT':
                user_id = request.data.get('user_id', 0)
                if str(user.id) == str(user_id):
                    return check_profile_owner(user)
        return False


# if the send user_id same as in token
class CheckUserPermission(BasePermission):
    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response:
            user, token = response
            if request.method == 'GET':
                user_id = request.GET.get('user_id', 0)
                if str(user.id) == str(user_id):
                    return True
        return False
