from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # override has_object_permission method as per instructor
    def has_object_permission(self, request, view, obj):
        # First check user is requesting only readonly access then return true
        if request.method in permissions.SAFE_METHODS:
            return True
        # else only the user making request owns the profile
        return obj.owner == request.user