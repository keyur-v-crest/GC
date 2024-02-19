from rest_framework.permissions import BasePermission 
from rest_framework.exceptions import PermissionDenied 
import random 
import string 

class CheckUserAuthentication(BasePermission):
    def has_permission(self, request, view):

        if request.user.is_authenticated == True:
            return True
        else:
            raise PermissionDenied({
                'status': False, 
                'message': "User don't have permission for this route"
            })
        
def HelperCreateFamilyId():
    # Generate 4 random characters
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=4))

    # Generate 2 random digits
    random_digits = ''.join(random.choices(string.digits, k=2))

    # Concatenate the random characters and digits
    result = random_chars + random_digits 

    return result