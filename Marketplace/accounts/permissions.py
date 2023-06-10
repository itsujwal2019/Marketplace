from rest_framework.permissions import BasePermission

class IsModeratorUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "moderator"
