
from rest_framework.permissions import BasePermission
from users.constants import ROLE_ADMIN, ROLE_SALES_USER

message = "You do not have permission to perform this action."

class IsAdmin(BasePermission):
    message = message

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == ROLE_ADMIN)


class IsSales(BasePermission):
    message = message

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == ROLE_SALES_USER)