from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


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
            elif request.method in ('DELETE', 'POST'):
                user_id = request.data.get('user_id', 0)
                if str(user.id) == str(user_id):
                    return True
        return False


class AdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response:
            user, token = response
            return True if user.is_admin else False
        return False