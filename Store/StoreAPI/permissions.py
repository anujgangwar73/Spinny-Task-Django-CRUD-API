from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class CanUpdateBox(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            # Staff users can update any box
            return True
        return False

class CanViewBox(permissions.BasePermission):
    def has_permission(self, request, view):
        return True  # Allow any authenticated or unauthenticated user to view boxes

class CanViewMyBoxes(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is staff and can view their own boxes
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Check if the user is staff and the box belongs to them
        return request.user.is_staff and obj.creator == request.user


class CanDeleteBox(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the creator of the box
        return obj.creator == request.user