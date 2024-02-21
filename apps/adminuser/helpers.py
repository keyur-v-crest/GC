from rest_framework.permissions import BasePermission 
from rest_framework.exceptions import PermissionDenied 

class CheckAdminUser(BasePermission): 
    def has_permission(self, requets, view):
        print("Run this functionality") 
        print(requets.user)