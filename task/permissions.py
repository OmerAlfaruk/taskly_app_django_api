from rest_framework import permissions

class IsAllowedToEditTaskListOrNone(permissions.BasePermission):
    """ Custom permission to only allow creators of a task list to edit it."""
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:

            # Allow GET/HEAD/OPTIONS for everyone
            return True
        if not request.user.is_anonymous:
            return True
        return False
    

    def has_object_permission(self, request, view, obj):
            
            return request.user == obj.created_by
           

class IsAllowedToEditTaskOrNone(permissions.BasePermission):
    """ Custom permission to only allow creators of a task to edit it."""
    def has_permission(self,request,view):
        
        if not request.user.is_anonymous:
            return request.user.profile.house!=None
        return False
           
   

    def has_object_permission(self, request, view, obj):
            
            return request.user.profile.house == obj.task_list.house
        
    
class IsAllowedToEditAttachmentsOrReadOnly(permissions.BasePermission):
    """ Custom permission to only allow creators of an attachment to edit it."""
    def has_permission(self,request,view):
        if not request.user.is_anonymous:
            return request.user.profile.house!=None
        return False
           
   

    def has_object_permission(self, request, view, obj):
            
            return request.user.profile.house == obj.task.task_list.created_by.house
