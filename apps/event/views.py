from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication 
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response
from datetime import datetime, timedelta
from apps.event.models import Details as Event_details 
from apps.user.models import Event as User_event_model
from apps.event.models import Gallery as Event_gallery_model
from apps.event import serializer
from django.conf import settings
from apps.event import helpers as event_helpers
from django.db.models import Count
import stripe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from apps.event.models import Gallery as Event_gallery_model

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_upcominglist_view(request): 
    try:
        today_date = datetime.today() 
        seven_days_from_now = datetime.now().date() + timedelta(days=7)
        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        # All latest event data information 
        Event_information = Event_details.objects.filter(publish_date__range=[today_date, seven_days_from_now])
        Event_information_paginator = Paginator(Event_information, page_size)

        try:
            Event_information_paginator_page = Event_information_paginator.page(page_number)
        except EmptyPage:
            Event_information_paginator_page = []
        Event_information_paginator_page_data = serializer.SerializerEventDetails(Event_information_paginator_page, many = True)

        return Response({
            'status': True, 
            'message': 'Fetch', 
            'data': Event_information_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_featuredlist_view(request):
    try:
        seven_days_from_now = datetime.now().date() + timedelta(days=7)
        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        if "category" in request.query_params:
            Event_information = Event_details.objects.filter(publish_date__gte = seven_days_from_now, category_id = request.query_params.get("category"))
        else:
            Event_information = Event_details.objects.filter(publish_date__gte = seven_days_from_now)
        Event_information_paginator = Paginator(Event_information, page_size)

        try:
            Event_information_paginator_page = Event_information_paginator.page(page_number)
        except EmptyPage:
            Event_information_paginator_page = []
        Event_information_paginator_page_data = serializer.SerializerEventDetails(Event_information_paginator_page, many = True)

        return Response({
            "status": True,
            "message": "Fetch", 
            "data": Event_information_paginator_page_data.data
        }, status=200) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_details_view(request, id): 
    try:

        # Fetch particular event details 
        Particular_event_details = Event_details.objects.get(id =id)
        status, member_count, member_information = event_helpers.helper_get_event_joined_members(request.query_params.get("id"))
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": {
                "event_image": Particular_event_details.event_image, 
                "event_name": Particular_event_details.event_name, 
                "event_address": Particular_event_details.event_address, 
                "event_address_latitude": Particular_event_details.event_address_latitude, 
                "event_address_longitude": Particular_event_details.event_address_longitude, 
                "event_date": Particular_event_details.event_date, 
                "event_start_time": Particular_event_details.event_start_time, 
                "event_end_time": Particular_event_details.event_end_time, 
                "organizer_image": Particular_event_details.organizer_image, 
                "organizer_name": Particular_event_details.organizer_name, 
                "organizer_contact": Particular_event_details.organizer_contact_number, 
                "event_description":  Particular_event_details.event_description, 
                "event_price": Particular_event_details.price , 
                "is_vip_seat": Particular_event_details.is_vip_seat,
                "member_count": member_count, 
                "member_information": member_information
            }
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)    

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_payment_view(request):

    try:

        if serializer.SerializerEventPayment(data = request.data).is_valid():

            # Check numberOf exists or not 
            booking_status = event_helpers.helper_check_number_of_seat(request.data['event_id'], request.data['booking_count'])

            if booking_status:
                user_list = request.data['family_member']
                user_list.insert(0, request.user.id) 
                for item in user_list:
                    status = event_helpers.helper_user_event_status_check(request.data['event_id'], item)
                    if not status: 
                        return Response({
                            'status': False, 
                            "message": "One member already booked for this event. Please check that"
                        }, status=400)
                    

                # Confiure stripe api key 
                stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

                # Metadata information 
                metadata = {
                    "event_id": request.data['event_id'], 
                    "event_type": request.data['event_type'], 
                    "event_user": json.dumps(user_list), 
                    "type": "event"
                }

                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': request.data['event_name'],
                                },
                                'unit_amount':int(request.data['event_price'])*100,
                            },
                            'quantity': 1,
                        },
                    ],
                    metadata=metadata,
                    mode='payment',
                    success_url='http://localhost:8000/success/',
                    cancel_url='http://localhost:8000/cancel/',
                    client_reference_id = request.user.id
                )
                # Create enrty in user event table 
                for item in user_list:
                    User_event_model.objects.get_or_create(
                        family_id=request.user.family_id,
                        event_id=request.data['event_id'],
                        user_id=item,
                        book_by_id=request.user.id,
                        event_type=request.data['event_type'],
                        defaults={'ticket_number': event_helpers.helper_get_ticket_number()}
                    )


                return Response({
                    'status': True, 
                    'message': "Create", 
                    "data": session.url
                }, status=200)  
            else:
                return Response({
                    "status" : False, 
                    "messgae": "All seat already booked for this event"
                }, status=400)
        else:
            return Response({
                'status': False, 
                'message': "Failed to created payment session"
            }, status=400)
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_ticketdetails_view(request, id):
    try:

        # Fetch particular event details 
        Particular_event_details = Event_details.objects.get(id =id)
        
        # Fetch joined user count 
        Fetch_joined_user = User_event_model.objects.filter(book_by_id = request.user.id, event_id = id, transaction_status = "Complete").count()
        
        # Ticket number 
        Ticket_number = User_event_model.objects.filter(user_id = request.user.id, event_id = id, transaction_status = "Complete").values("ticket_number")
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data":{
                "event":{
                    "event_image": Particular_event_details.event_image, 
                    "event_name": Particular_event_details.event_name, 
                    "organizer_name": Particular_event_details.organizer_name, 
                    "event_date": Particular_event_details.event_date, 
                    "event_start_time":  Particular_event_details.event_start_time, 
                    "event_end_time": Particular_event_details.event_end_time, 
                    "event_address": Particular_event_details.event_address, 
                    "event_address_latitude": Particular_event_details.event_address_latitude, 
                    "event_address_longitude": Particular_event_details.event_address_longitude
                }, 
                "joined_member": Fetch_joined_user, 
                "ticket_information": Ticket_number
            }
        }, status=200) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_history_view(request):
    try:

        if serializer.event_history_serializer(data = request.query_params).is_valid():

            response = []
            if request.query_params.get("status") == "all": 
                user_event_ids = User_event_model.objects.filter(user_id=request.user.id).select_related("event").order_by("-id")

            elif request.query_params.get("status") == "Upcoming": 
                user_event_ids = User_event_model.objects.filter(user_id=request.user.id, status = "Upcoming").select_related("event").order_by("-id")
            
            else:
                user_event_ids = User_event_model.objects.filter(user_id=request.user.id, status = "Completed").select_related("event").order_by("-id")

            user_event_id_paginator = Paginator(user_event_ids, int(request.query_params.get("page_size")))
            user_event_paginator_page = user_event_id_paginator.get_page(int(request.query_params.get("page_number")))
            user_event_paginator_page_data = serializer.UserEventListFechSerializer(user_event_paginator_page, many  =True)
            
            return Response({
                'status': True, 
                "message": "Fetch", 
                "data":user_event_paginator_page_data.data
            }, status=200)
        else:
            return Response({
                'status': False, 
                "mesasge": "Failed to fetch event history"
            }, status=400) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_recentgallery_view(request):
    try:

        today_date = datetime.today() 
        seven_days_from_now = datetime.now().date() + timedelta(days=7)

        User_event_gallery = User_event_model.objects.filter(user_id = request.user.id, status = "Complete", event__event_date__range=[today_date, seven_days_from_now])
        User_event_gallery = serializer.EventGalleryListSerializer(User_event_gallery, many = True)

        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": User_event_gallery.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_otheralubms_view(request):
    try:

        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size")) 

        User_event_gallery = User_event_model.objects.filter(user_id = request.user.id, status="Complete").order_by("-id")
        User_event_gallery_paginator = Paginator(User_event_gallery, page_size)

        try:
            User_event_gallery_paginator_page = User_event_gallery_paginator.page(page_number)
        except EmptyPage:
            User_event_gallery_paginator_page = User_event_gallery_paginator.page(0)
        
        User_event_gallery_paginator_page_data = serializer.EventGalleryListSerializer(User_event_gallery_paginator_page, many = True)

        return Response({
            "status": True,
            "message": "Fetch", 
            "data": User_event_gallery_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_imagefile_view(request, id):
    try:

        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        Event_images = Event_gallery_model.objects.filter(event_id = id).order_by("-id")
        Event_images_paginator = Paginator(Event_images, page_size)
        
        try: 
            Event_images_paginator_page = Event_images_paginator.page(page_number)
        except EmptyPage:
            Event_images_paginator_page = []
        
        Event_images_paginator_page_data = serializer.EventImageSerializer(Event_images_paginator_page, many = True)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": Event_images_paginator_page_data.data
        }, status=200) 
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_date_view(request):
    try:

        if serializer.EventDateWiseSerializer(data = request.data).is_valid():
            user_id = request.user.id 
            month = request.data['month']
            year = request.data['year']

            user_date_wise_event = (
                User_event_model.objects
                .filter(user_id=user_id, event__event_date__year=year, event__event_date__month=month)
                .values('event__event_date')
                .annotate(count=Count('id'))
                .order_by('event__event_date')
                .values('event__event_date', 'count')
            )

            return Response({
                'status': True, 
                "message" : "Fetch", 
                "data": user_date_wise_event
            }, status=200)
        
        else:
            return Response({
                'status': False, 
                "message": "Network request failed"
            }, status=500)
    except Exception as e : 
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_particulardate_view(request):
    try:
        date = request.data['date']
        User_particular_date_event = User_event_model.objects.filter(user_id = request.user.id, event__event_date = date, status = "Upcoming").order_by("-id")
        User_particular_date_event = serializer.EventDateWiseData(User_particular_date_event, many = True)
        return Response({
            'status': True, 
            "message": "Fetch", 
            "data": User_particular_date_event.data
        }, status=200) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_gallery_view(request, id):
    try:
        Event_images = Event_gallery_model.objects.filter(event_id = id).order_by("-id")
        Event_images_paginator = Paginator(Event_images, int(request.query_params.get("page_size")))
        Event_image_paginator_page = Event_images_paginator.get_page(int(request.query_params.get("page_number")))
        Event_image_paginator_page_data = serializer.EventImageDataSerializer(Event_image_paginator_page, many = True)
        return Response({
            'status': True, 
            "message": "Fetch", 
            "data": Event_image_paginator_page_data.data
        }, status=200) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_filter_view(request):
    try:
        
        filter_status = request.query_params.get("status")
        User_filter_event = User_event_model.objects.filter(user_id = request.user.id, status = filter_status).order_by("-event__event_date")
        User_filter_event_paginator = Paginator(User_filter_event, int(request.query_params.get("page_size")))
        User_filter_event_paginator_page = User_filter_event_paginator.get_page(int(request.query_params.get("page_number")))
        User_filter_event_paginator_page_data = serializer.EventFilterDataSerializer(User_filter_event_paginator_page, many = True)
        return Response({
            'status': True, 
            'message': "Fetch", 
            "data":User_filter_event_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            'status': False, 
            "message": "Network request failed"
        }, status=500) 
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_ticketlist_view(request): 
    try:

        User_ticket = User_event_model.objects.filter(user_id = request.user.id, status = "Upcoming", transaction_status = "Complete").order_by("-event__event_date")
        User_ticket_paginator = Paginator(User_ticket, int(request.query_params.get("page_size")))
        User_ticket_paginator_page = User_ticket_paginator.get_page(int(request.query_params.get("page_number")))
        User_ticket_paginator_page_data = serializer.EventTicketDataSerializer(User_ticket_paginator_page, many = True)
        return Response({
            'status': True, 
            "message": "Fetch", 
            "data": User_ticket_paginator_page_data.data
        })
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_historylist_view(request):
    try:
        filter_value = request.query_params.get("option") 
        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        if filter_value == "upcoming" :
            User_events = User_event_model.objects.filter(user_id = request.user.id, status = "Upcoming").order_by("-event__event_date")
        else:
            print("Run this")
            User_events = User_event_model.objects.filter(user_id = request.user.id, status = "Complete").order_by("-event__event_date")
        
        User_events_paginator = Paginator(User_events, page_size)

        try:
            User_events_paginator_page = User_events_paginator.page(page_number)
        except EmptyPage: 
            User_events_paginator_page = [] 
        
        User_events_paginator_page_data = serializer.UserEventListFechSerializer(User_events_paginator_page, many = True)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": User_events_paginator_page_data.data
        }, status=200)
    except Exception as e:
        print("Error message information ========>")
        print(e)
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

