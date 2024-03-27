from django.shortcuts import render
from apps.user.serializer import SerializerCreateUserStep1, SerializersCreateUserStep2, SerializersCreateUserStep3, SerializersCreateUserStep4
from apps.user import serializer
from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from apps.user.models import Details as User_details
from apps.user.models import Achievments as Achievments_model
from django.contrib.auth.hashers import make_password, check_password 
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from apps.user.helpers import HelperCreateFamilyId, CheckUserAuthentication,  HelperGeneratePassword
from rest_framework_simplejwt.authentication import JWTAuthentication 
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(["POST"])
def RouteUserSignStep1(request): 
    try:

        if SerializerCreateUserStep1(data = request.data).is_valid():

            Email_check = User_details.objects.filter(email = request.data['email']).count() 

            if Email_check > 0: 
                
                User_object = User_details.objects.get(email = request.data['email'])  
                
                if not User_object.step2: 
                    return Response({
                        'status': False, 
                        'message': "Step2 not complete"
                    }, status = 400)

                if not User_object.step3: 
                    return Response({
                        'status': False, 
                        'message': "Step3 not complete"
                    }, status=400)
                
                if not User_object.step4:
                    return Response({
                        'status': False, 
                        'message': "Step4 not complete"
                    }, status=400)
                
                if not User_object.email_verified: 
                    return Response({
                        'status': False, 
                        'message': "Email not verified"
                    }, status=400)
                
                if not User_object.mobile_verified: 
                    return Response({
                        'status': False, 
                        'message': "Mobile number not verified"
                    }, status=400)
                
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
                    family_id = HelperCreateFamilyId(), 
                    step1 = True
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
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteUserSignupStep2(request): 
    try:

        if SerializersCreateUserStep2(data = request.data).is_valid(): 

            User_details.objects.filter(id = request.user.id).update(gender = request.data['gender'], step2 = True)

            return Response({
                'status': True, 
                'message': "Step2 complete"
            }, status=200)
        else:
            return Response({
                'status': False, 
                'message': "Failed to complete step2"
            }, status=400)
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500) 
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteUserSignupStep3(request): 
    try:

        if SerializersCreateUserStep3(data = request.data).is_valid():

            # Email check 
            Email_check = User_details.objects.filter(email = request.data['email']).count() 

            if Email_check > 0 : 
                return Response({
                    'status': False, 
                    "message": "Already create account with this email address"
                }, status=400)

            else:

                User_details.objects.filter(id = request.user.id).update(step3 = True) 

                # New member 
                New_member = User_details.objects.create(
                    first_name = request.data['first_name'], 
                    last_name = request.data['last_name'], 
                    email = request.data['email'], 
                    mobile = request.data['mobile_number'], 
                    profession = request.data['profession'], 
                    profession_description = request.data['description'], 
                    address = request.data['address'], 
                    relation = request.data['relation'], 
                    username = str(uuid.uuid4()), 
                    family_id = request.user.family_id, 
                    sub_member = True, 
                    password = make_password(HelperGeneratePassword())
                )

                New_member.save()

                return Response({
                    'status': True, 
                    'messgae': "Family member add"
                }, status=200) 
        else: 
            return Response({
                'status': False, 
                'message': "Failed to add family member"
            }, status=400)
        
    except Exception as e:

        return Response({
            'status': False, 
            "message": "Network request failed"
        }, status=500)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RotueUserSignupStep4(request): 
    try:

        if SerializersCreateUserStep4(data = request.data).is_valid():

            User_details.objects.filter(id = request.user.id).update(
                profile_image = request.data['profile_image'], 
                step4 = True    
            )
            
            return Response({
                'status': True, 
                'message': "Step4 complete"
            }, status=200)
        
        else:

            return Response({
                'status': False, 
                'message': "Failed to update profile image"
            }, status=400)
        
    except Exception as e:

        return Response({
            'status': False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["POST"])
def RouteUserLogin(request):
    try:

        if SerializerUserLogin(data = request.data).is_valid():

            pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' 
            mobile_number_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$'

            try: 

                User_object = None
                if re.match(pattern, request.data['username']):
                    User_object = User_details.objects.get(email = request.data['username']) 
                elif re.match(mobile_number_pattern, request.data['username']): 
                    User_object = User_details.objects.get(mobile = request.data['username']) 
                else:
                    User_object = User_details.objects.get(family_id = request.data['username'])

                if not User_object.step2: 
                    return Response({
                        'status': False, 
                        'message': "Your signup process in not complete. Complete first"
                    }, status=400) 
                
                if not User_object.step3: 
                    return Response({
                        'status': False, 
                        'message': "Your signup process in not complete. Complete first"
                    }, status=400) 
                
                if not User_object.step4:
                    return Response({
                        'status': False, 
                        'message': "Your signup process in not complete. Complete first"
                    }, status=400) 
                
                if not User_object.mobile_verified: 
                    return Response({
                        'status': False, 
                        'message': "Your mobile number verification is pending"
                    }, status=400)

                if not User_object.email_verified: 
                    return Response({
                        'status': False, 
                        'message': "Your email verification is pending"
                    }, status=400)
                
                # Check password 
                
                if check_password(request.data['password'], User_object.password): 

                    Refersh_token = RefreshToken.for_user(User_object)

                    return Response({
                        'status': True,
                        'message': "Login", 
                        "data": {
                            "access_token": str(Refersh_token.access_token)
                        }
                    }, status=200)
                else:
                    return Response({
                        'status': False, 
                        'message': "Invalid Password"
                    }, status=400)
        
            except Exception as e:
                return Response({
                    'status': False, 
                    'message': "User not found"
                }, status=400)
        else:
            
            return Response({
                'status': False, 
                'message': "Failed to login"
            }, status=400)

    except Exception as e:

        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteFetchFamilyMembers(request): 
    try:
        # Fetch all family member information based on family id 
        Family_members = User_details.objects.filter(family_id = request.user.family_id).exclude(id = request.user.id)
        Family_members = serializer.SerializerFetchFamilyMemberInfo(Family_members, many = True)

        return Response({
            'status': True, 
            'message':  'Fetch', 
            'data': Family_members.data
        }, status=200)
    except Exception as e: 
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def achievment_create_view(request):
    try:
        if serializer.AcheivementCreateSerializer(data = request.data).is_valid():
            
            User_check = Achievments_model.objects.filter(user_id = request.user.id).count() 

            if User_check == 0:
                Achievments_model.objects.create(
                    user_id = request.user.id, 
                    name = request.data['name'], 
                    count = len(request.data['name'])
                )
            else:
                Achievments_model.objects.filter(user_id  = request.user.id).update(
                    name = request.data['name'], 
                    count = len(request.data['name'])
                )
            return Response({
                "status": True, 
                "message": "Create"
            }, status=200) 
        else:
            return Response({
                "status": False, 
                "message": "Failed to create Achievment"
            }, status=400)
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
        
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def achievment_list_view(request):
    try:

        User_achivement_list = Achievments_model.objects.filter(user_id = request.user.id).values("name")
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": User_achivement_list
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)

import random
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def achivement_screen_list_view(request):
    try:

        Random_achivers = Achievments_model.objects.all() 
        Random_achivers_data = Random_achivers[:10]
        Random_achivers_data = serializer.AchivementListSerializer(Random_achivers_data, many = True)
        
        return Response({
            "status": True,
            "message": "Fetch", 
            "data": Random_achivers_data.data
        }, status=400)
    except Exception as e:
        return Response({
            'status': False, 
            "message":"Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def achiever_list_view(request):
    try:

        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get('page_size'))
        count_sort = (request.query_params.get('count_sort'))

        if count_sort == "yes":
            Achiever_list = Achievments_model.objects.all().order_by("-count")
        else:
            Achiever_list = Achievments_model.objects.all().order_by("-id")
        Achiever_list_paginator = Paginator(Achiever_list, page_size)

        try:
            Achiever_list_paginator_page = Achiever_list_paginator.page(page_number)
        except EmptyPage: 
            Achiever_list_paginator_page = []

        Achiever_list_paginator_page_data = serializer.AchieverListSerializer(Achiever_list_paginator_page, many = True)

        return Response({
            "status": True,
            "message": "Fetch", 
            "data": Achiever_list_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def achivement_details_view(request, id):
    try:

        Achievment_object = Achievments_model.objects.get(id = id)
        return Response({
            "status": True,
            "message": "Fetch", 
            "data": {
                "background_image": Achievment_object.user.background_image, 
                "username": Achievment_object.user.first_name, 
                "count": Achievment_object.count, 
                "achivement": Achievment_object.name, 
                "profession": Achievment_object.user.profession, 
                "profession_description": Achievment_object.user.profession_description
            }
        }, status=200) 
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)

    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def user_profiiledetails_view(request):
    try:

        # Reterive user achivement 
        User_achivements = Achievments_model.objects.filter(user_id = request.user.id).values("name")
        return Response({
            "status": True,
            "message": "Fetch", 
            "data": {
                "profile_image": request.user.profile_image, 
                "username": request.user.first_name, 
                "dob": request.user.dob, 
                "email": request.user.email, 
                "gender": request.user.gender, 
                "address": request.user.address,
                "profession": request.user.profession, 
                "linkdin": request.user.linkdin, 
                "upwork": request.user.upwork, 
                "background_image": request.user.background_image, 
                "achivements": User_achivements
            }
        })
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def user_profile_update_view(request):
    try:

        if serializer.ProfileUpdateSerializer(data = request.data).is_valid(): 

            # Check email 
            Check_email = User_details.objects.filter(email = request.data['email']).exclude(id = request.user.id).count()

            if Check_email == 0 :
                User_object = User_details.objects.get(id = request.user.id)
                User_object.profile_image = request.data['user_image']
                User_object.first_name = request.data['username']
                User_object.dob = request.data['dob']
                User_object.email = request.data['email']
                User_object.gender = request.data['gender']
                User_object.address = request.data['address']
                User_object.profession = request.data['profession']
                User_object.linkdin = request.data['linkdin']
                User_object.upwork = request.data['upwork']
                User_object.background_image = request.data['background_image']
                User_object.save()

                return Response({
                    "status": True,
                    "message": "Update"
                }, status=200)
            
            else:
                return Response({
                    "status": False, 
                    "message": "Failed to update user profile"
                }, status=400)
        else:
            return Response({
                "status": True, 
                "message": "Failed to update"
            }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)