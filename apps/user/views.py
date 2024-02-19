from django.shortcuts import render
from apps.user.serializer import SerializerCreateUserStep1 
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from apps.user.models import Details as User_details
from django.contrib.auth.hashers import make_password, check_password 
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from apps.user.helpers import HelperCreateFamilyId

@api_view(["POST"])
def RouteUserSignStep1(request): 
    try:

        if SerializerCreateUserStep1(data = request.data).is_valid():

            Email_check = User_details.objects.filter(email = request.data['email']).count() 

            if Email_check > 0: 
                return Response({
                    'status': False, 
                    'message': "Already have account with this emailaddress"
                }, status=400)
            else:

                Create_user =  User_details.objects.create(
                    username = str(uuid.uuid4()), 
                    email = request.data['email'], 
                    first_name = request.data['first_name'], 
                    last_name = request.data['last_name'], 
                    password = make_password(request.data['password']), 
                    mobile = request.data['mobile_number'], 
                    dob = request.data['dob'], 
                    address = request.data['address'], 
                    profession = request.data['profession'], 
                    profession_description = request.data['description'], 
                    family_id = HelperCreateFamilyId()
                )
                Create_user.save()

                Refersh_token = RefreshToken.for_user(Create_user)

                return Response({
                    'status': True, 
                    "message": "Create user", 
                    "data": {
                        "access_token": str(Refersh_token.access_token)
                    }
                }, status=200)
        else:
            return Response({
                'status': False, 
                'message': "Failed to create user"
            }, status=400)
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)