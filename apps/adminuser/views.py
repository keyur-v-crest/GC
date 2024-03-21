from apps.adminuser import serializer 
from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication 
from apps.user.models import Details as User_details 
from apps.user.helpers import CheckUserAuthentication
import uuid
from apps.event.models import Details as Event_details 
from apps.event.models import Gallery as Event_gallery
from django.core.paginator import Paginator 
from datetime import datetime

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
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteCreateEvent(requets): 
    try:

        if serializer.SerializerCreateEvent(data = requets.data).is_valid():

            # Create new event 
            New_event = Event_details.objects.create(
                event_name = requets.data['event_name'], 
                event_description = requets.data['event_description'], 
                category_id = requets.data['category'], 
                price = requets.data['price'], 
                event_date = requets.data['event_date'], 
                publish_date = requets.data['publish_date'], 
                event_start_time = requets.data['event_start_time'], 
                event_end_time = requets.data['event_end_time'], 
                event_address = requets.data['event_address'], 
                event_address_latitude = requets.data['event_address_latitude'], 
                event_address_longitude = requets.data['event_address_longitude'], 
                event_image = requets.data['event_image'], 
                number_of_people = requets.data['number_of_people'], 
                number_of_seat = requets.data['number_of_seat'], 
                organizer_name = requets.data['organizer_name'], 
                organizer_contact_number = requets.data['organizer_contact_number'], 
                organizer_description = requets.data['organizer_description'], 
                event_create_by_id = requets.user.id, 
                organizer_image = requets.data['organizer_image'], 
                event_type = requets.data['event_type']
            )

            # Store event gallery information 
            event_gallery_bulk_insert = []

            for item in requets.data['event_gallery']:
                event_type = item['type']
                event_image = item['value']
                event_gallery_bulk_insert.append(
                    Event_gallery(
                        event_id = New_event.id, 
                        type = event_type, 
                        link = event_image
                    )
                )
            Event_gallery.objects.bulk_create(event_gallery_bulk_insert)

            return Response({
                'status': True, 
                'message': 'Create'
            }, status=200)
        else: 
            return Response({
                'status': False, 
                "message": "Failed to create event"
            }, status=400)
    except Exception as e: 

        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=400)
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteGetEventDetails(request):
    try:

        if serializer.SerializerPaginator(data = request.data).is_valid():

            # Event details 
            All_event = Event_details.objects.all().order_by("-id") 
            All_event_paginator = Paginator(All_event, request.data['page_size'])
            All_event_paginator_page = All_event_paginator.get_page(request.data['page_number'])
            All_event_paginator_page = serializer.SerializerFetchEventList(All_event_paginator_page, many = True)

            return Response({
                'status': True, 
                "message": "Fetch", 
                "data" : All_event_paginator_page.data
            }, status=200)
        else: 
            return Response({
                "status": False,
                'message': "Failed"
            }, status=400)
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=400) 
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteGetParticularEventDetails(request): 
    try:

        if serializer.SerializersFetchParticularEventDetails(data = request.data).is_valid():
            
            Particular_event_details = Event_details.objects.get(id = request.data['id'])
            return Response({
                'status': True, 
                'message': "Fetch", 
                "data": {
                    "id": Particular_event_details.id, 
                    "event_name": Particular_event_details.event_name, 
                    "event_description": Particular_event_details.event_description, 
                    "category": Particular_event_details.category_id, 
                    "event_date": Particular_event_details.event_date, 
                    "event_start_time": Particular_event_details.event_start_time, 
                    "event_end_time": Particular_event_details.event_end_time, 
                    "event_address": Particular_event_details.event_address, 
                    "event_address_latitude": Particular_event_details.event_address_latitude, 
                    "event_address_longitude": Particular_event_details.event_address_longitude, 
                    "number_of_people": Particular_event_details.number_of_people, 
                    "number_of_seat": Particular_event_details.number_of_seat, 
                    "organizer_name": Particular_event_details.organizer_name, 
                    "organizer_contact_number": Particular_event_details.organizer_contact_number, 
                    "organizer_description": Particular_event_details.organizer_description, 
                    "price": Particular_event_details.price
                }
            }, status=200)
        
        else:
        
            return Response({
                "status": False,
                'message': "Failed"
            }, status=400)
        
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=400)  
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteUpdateEventDetails(request): 
    try:

        if serializer.SerializerUpdateEvent(data = request.data).is_valid():

            # Particular event object 
            Particular_event_object = Event_details.objects.get(id = request.data['id'])
            Particular_event_object.event_name = request.data['event_name']
            Particular_event_object.event_description = request.data['event_description']
            Particular_event_object.price = request.data['price']
            Particular_event_object.event_date = request.data['event_date']
            Particular_event_object.publish_date = request.data['publish_date']
            Particular_event_object.event_start_time = request.data['event_start_time']
            Particular_event_object.event_end_time = request.data['event_end_time']
            Particular_event_object.event_address = request.data['event_address']
            Particular_event_object.event_address_latitude = request.data['event_address_latitude']
            Particular_event_object.event_address_longitude = request.data['event_address_longitude'] 
            Particular_event_object.event_image = request.data['event_image'] 
            Particular_event_object.number_of_people   = request.data['number_of_people']
            Particular_event_object.organizer_name = request.data['organizer_name']
            Particular_event_object.organizer_contact_number = request.data['organizer_contact_number']
            Particular_event_object.organizer_description = request.data['organizer_description']
            Particular_event_object.number_of_seat = request.data['number_of_seat']
            Particular_event_object.organizer_image = request.data['organizer_image']
            Particular_event_object.event_type = request.data['event_type']
            Particular_event_object.save()

            return Response({
                'status': True,
                'mesasge': 'Update'
            }, status=200) 
        else: 
            return Response({
                'status' : False, 
                'message': "Failed"
            }, status=400)
    except Exception as e:

        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=400)  
        

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_latest_view(request):
    try:

        Event_list = Event_details.objects.all().order_by("-id")
        Event_list_paginator = Paginator(Event_list, int(request.query_params.get("page")))

        return Response({
            "status": True, 
            "message": "Fetch"
        }, status=200)
    except Exception as e:
        return Response({
            'status': False, 
            "message": "Network request failed"
        }, status=500)