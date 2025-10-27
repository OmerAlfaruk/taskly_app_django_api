from rest_framework import permissions

# class IsHouseManagerOrNone(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#            return True
       
#         if not request.user.is_anonymous:
#            return True
#         return False

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         return request.user == obj.manager


class IsHouseManagerOrNone(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET/HEAD/OPTIONS for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow only authenticated users to perform POST/DELETE/etc.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Manager is a Profile, so compare properly
        return hasattr(request.user, "profile") and obj.manager == request.user.profile
