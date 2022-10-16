from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.models import UserAccount

class AdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        response = request.data
        if response:
            username = response.get('username', '')
            password = response.get('password', '')

            try:
                user = UserAccount.objects.get(username=username)
                check_user = True if user.check_password(password) else False
                if check_user:
                    return user.is_admin
            except UserAccount.DoesNotExist:
                return False

        return False