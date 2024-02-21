from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication 
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response
from datetime import datetime
from apps.event.models import Details as Event_details 
from apps.event import serializer

@api_view(["POST"])
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
    
