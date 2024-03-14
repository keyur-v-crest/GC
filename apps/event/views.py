from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication 
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response
from datetime import datetime
from apps.event.models import Details as Event_details 
from apps.event import serializer
from django.conf import settings
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
            return Response({
                "status": True, 
                "message": "Fetch"
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

        # Confiure stripe api key 
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        print(settings.STRIPE_TEST_SECRET_KEY)

        # Metadata information 
        metadata = {
            "order_id": "Order id information", 
            "client_reference_id": 1
        }

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'T-shirt',
                        },
                        'unit_amount': 2000,
                    },
                    'quantity': 1,
                },
            ],
            metadata=metadata,
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )

        print(session.url)

        return Response({
            'status': True, 
            'message': "Create"
        }, status=200)
    except Exception as e:

        print("Error message information ==========>")
        print(e)

        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)