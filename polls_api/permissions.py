from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # 'GET', 'HEAD', 'OPTIONS'
            return True
        return obj.owner == request.user
        #return super().has_object_permission(request, view, obj)

class IsVoter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.voter == request.user
