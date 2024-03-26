from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response
from apps.donation.models import Details as Donation_details 
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from apps.donation import serializer

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def donation_list_view(request):
    try:
        today_date = datetime.today()
        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        Donation_list = Donation_details.objects.filter(donation_end_date__gte=today_date, donation_start_date__lte=today_date).order_by("-id")
        Donation_list_paginator = Paginator(Donation_list, page_size)

        try:
            Donation_list_paginator_page = Donation_list_paginator.page(page_number)
        except EmptyPage:
            Donation_list_paginator_page = []

        Donation_list_paginator_page_data = serializer.DonationListSerializer(Donation_list_paginator_page, many = True)

        return Response({
            "status": True,
            "message": "Fetch", 
            "data": Donation_list_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def donation_details_view(request, id):
    try:

        Donation_object = Donation_details.objects.get(id = id)
        
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data":{
                "image": Donation_object.image,
                "donation_name": Donation_object.donation_name, 
                "organizer_name": Donation_object.organizer_name, 
                "organizer_image": Donation_object.organizer_image,
                "organizer_contact": Donation_object.organizer_contact, 
                "description": Donation_object.description
            }
        }, status=200) 
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
