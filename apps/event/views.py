from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication 
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response
from datetime import datetime
from apps.event.models import Details as Event_details 
from apps.user.models import Event as User_event_model
from apps.event import serializer
from django.conf import settings
from apps.event import helpers as event_helpers
import stripe

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteFetchEvent(request): 
    try:

        # Curernt date 
        today_date = datetime.today() 

        # All latest event data information 
        Event_information = Event_details.objects.filter(publish_date__gte=today_date)
        Event_information = serializer.SerializerEventDetails(Event_information, many = True)

        return Response({
            'status': True, 
            'message': 'Fetch', 
            'data': Event_information.data
        }, status=200)
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def GetEventByIdRoute(request): 
    try:

        if serializer.SerializerParticularEventDetails(data = request.query_params).is_valid():

            # Fetch particular event details 
            Particular_event_details = Event_details.objects.get(id = request.query_params.get("id"))
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
                    "organizer_description": Particular_event_details.organizer_description, 
                    "event_description":  Particular_event_details.event_description, 
                    "event_price": Particular_event_details.price , 
                    "event_type": Particular_event_details.event_type
                }
            }, status=200)
        else:
            return Response({
                'status': False, 
                'message': "Failed to fetch event details"
            }, status=400)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)    

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def RouteEventPayment(request):
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
                    "event_type": request.data['event_type']
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
                User_event_check = User_event_model.objects.filter(event_id = request.data['event_id'], user_id = request.user.id).count()
                if User_event_check == 0:
                    User_event_model.objects.create(
                        family_id = request.user.family_id, 
                        event_id = request.data['event_id'], 
                        user_id = request.user.id, 
                        book_by_id = request.user.id, 
                        event_type = request.data['event_type']
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