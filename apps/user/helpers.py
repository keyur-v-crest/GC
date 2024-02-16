from rest_framework.permissions import BasePermission 
from rest_framework.exceptions import PermissionDenied 

class CheckUserAuthentication(BasePermission):
    def has_permission(self, request, view):

        if request.user.is_authenticated == True:
            return True
        else:
            raise PermissionDenied({
                'status': False, 
                'message': "User don't have permission for this route"
            })