from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response
from apps.donation.models import Details as Donation_details 
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from apps.donation import serializer
from django.conf import settings
import stripe
from apps.donation import helpers 

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
        print(e)
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
                "description": Donation_object.description, 
                "donation": helpers.get_donation_member_information(id)
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
def donation_payment_view(request):
    try:

        if serializer.DonationPaymentSerializer(data = request.data).is_valid():
            
            status = helpers.check_user_donation_entry(request.user.id, request.data['donation_id'], request.data['is_name_visible'])
            
            # Configure stripe api key 
            stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

            # Metadata information 
            metadata = {
                "donation_id": request.data['donation_id'], 
                "type": "donation", 
                "user_id": request.user.id
            }

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': request.data['donation_name'],
                                },
                                'unit_amount':int(request.data['amount'])*100,
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

            return Response({
                "status": True,
                "message": "Create", 
                "payment_url": session.url
            }, status=200) 
        else:
            return Response({
                "status": False,
                "message": "Failed to create payment"
            }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
