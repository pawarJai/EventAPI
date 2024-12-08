from rest_framework.permissions import BasePermission
from user.models import User


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        try:
            user = User.objects.get(email=request.user.email)
            return user.role == 'Admin'
        except User.DoesNotExist:
            return False
        
class IsUser(BasePermission):
    """
    Allows access only to regular users.
    """

    def has_permission(self, request, view):
        try:
            user = User.objects.get(email=request.user.email)
            return user.role == 'User'
        except User.DoesNotExist:
            return False
