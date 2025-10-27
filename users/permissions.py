from rest_framework import permissions
class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET and POST requests for any user
        return True

    def has_object_permission(self, request, view, obj):
        # Allow GET and POST requests for any user
        if request.method in permissions.SAFE_METHODS:
            return True
        # For other request methods, only allow if the user is the owner
        if not request.user.is_anonymous:
            return  request.user == obj
        return False
    

class IsProfileOwnerOrReadOnly(permissions.BasePermission):
     def has_permission(self, request, view):
         return True
     def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            if not request.user.is_anonymous:
                return request.user == obj.user
            return False
    