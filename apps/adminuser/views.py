from apps.adminuser import serializer 
from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated 
from apps.user.models import Details as User_details 
from apps.user.helpers import CheckUserAuthentication
import uuid

@api_view(["POST"])
def RouteCreateSuperUser(request): 
    try:

        if serializer.SerializerCreateSuperUser(data = request.data).is_valid():

            User_check = User_details.objects.filter(email = request.data['email'], is_admin = True).count() 

            if User_check > 0:
                return Response({
                    'status': False, 
                    'message': "Already create user with this emailaddress"
                }, status=400)
            else:
                New_user = User_details.objects.create(
                    username = str(uuid.uuid4()), 
                    email = request.data['email'], 
                    password = make_password(request.data['password']), 
                    is_superuser = request.data['is_superuser'], 
                    is_admin = True
                )    

                New_user.save()

                return Response({
                    'status': True,
                    'message': 'Create admin user successfully'
                }, status=200)
        else:
            return Response({
                'status': False, 
                "message": "Failed to create admin account"
            }, status=400)
        
    except Exception as e:
        
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

@api_view(["POST"])
def RouteAdminLogin(request): 
    pass 
    try:
        
        if serializer.SerializerUserLogin(data = request.data).is_valid():
            
            try: 

                User_object = User_details.objects.get(email = request.data['email'], is_admin = True)

                if check_password(request.data['password'], User_object.password):
                    
                    Refersh_token = RefreshToken.for_user(User_object)

                    return Response({
                        'status': True, 
                        'message': "Login successfully", 
                        'data': {
                            "access_token": str(Refersh_token.access_token)
                        }
                    }, status=200)
                else:
                    return Response({
                        'status': False, 
                        'message': "Invalid password"
                    }, status=400)
            except Exception as e: 
                return Response({
                    'status': False, 
                    'message': 'User not found'
                }, status=400)

        else:
            return Response({
                'stutus': False, 
                'message': "Failed to login"
            }, status=400)
    except Exception as e: 
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
        
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteGetAllAdmin(request):
    try:

        User_data = User_details.objects.filter(is_admin = True)
        User_data = serializer.SerializersUserFetch(User_data, many = True)
        
        return Response({
            'status': True, 
            "message": "Fetch", 
            "data": User_data.data
        }, status=200)
    except Exception as e:
        return Response({
            'status': False, 
            "message": "Network request failed"
        }, status=500)