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
from apps.user.models import Event as User_event_model 
from apps.donation.models import Details as Donation_model
from django.core.paginator import Paginator 
from djstripe.models import Session
import uuid
from apps.adminuser.models import Image
from django.conf import settings
from django.db.models import Sum

@api_view(["POST"])
def RouteAdminLogin(request): 
    try:
        if serializer.SerializerUserLogin(data = request.data).is_valid():
            try: 
                User_object = User_details.objects.get(email = request.data['email'], is_admin = True, is_superuser = request.data['is_superadmin'])
                if check_password(request.data['password'], User_object.password):
                    Refersh_token = RefreshToken.for_user(User_object)
                    return Response({
                        'status': True, 
                        'message': "Login successfully", 
                        'data': {
                            "access_token": str(Refersh_token.access_token), 
                            "first_name": User_object.first_name, 
                            "profile_image": User_object.profile_image
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
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def admin_check_view(request):
    try:
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data":{
                "first_name": request.user.first_name, 
                "profile_image": request.user.profile_image
            }
        }, status=200) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)

    
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
def event_create_view(requets): 
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
                number_of_seat = requets.data['number_of_seat'], 
                organizer_name = requets.data['organizer_name'], 
                organizer_contact_number = requets.data['organizer_contact_number'], 
                event_create_by_id = requets.user.id, 
                is_vip_seat = requets.data['is_vip_seat'], 
                event_address_city = requets.data['event_city'], 
                event_address_state = requets.data['event_state']
            )
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
def event_list_view(request):
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
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_details_view(request, id): 
    try:

        # Fetch particular event details 
        Particular_event_details = Event_details.objects.get(id = id)

        # Fetch total book seat information 
        Total_book_seat = User_event_model.objects.filter(event_id = id, transaction_status = "Complete").count()
        
        # Fetch total event earning information 
        Total_event_eaning = Session.objects.filter(metadata__contains={"event_id": str(id)}, payment_status ="paid").aggregate(total_earning=Sum("amount_total", default = 0))
        return Response({
            'status': True, 
            'message': "Fetch", 
            "data": {
                "id": Particular_event_details.id, 
                "event_image": Particular_event_details.event_image, 
                "event_name": Particular_event_details.event_name, 
                "event_description": Particular_event_details.event_description, 
                "category": Particular_event_details.category_id, 
                "event_date": Particular_event_details.event_date, 
                "event_publish_date": Particular_event_details.publish_date,
                "event_start_time": Particular_event_details.event_start_time, 
                "event_end_time": Particular_event_details.event_end_time, 
                "event_address": Particular_event_details.event_address, 
                "event_address_latitude": Particular_event_details.event_address_latitude, 
                "event_address_longitude": Particular_event_details.event_address_longitude, 
                "number_of_seat": Particular_event_details.number_of_seat, 
                "organizer_name": Particular_event_details.organizer_name, 
                "organizer_contact_number": Particular_event_details.organizer_contact_number, 
                "price": Particular_event_details.price, 
                "total_book_seat": int(Particular_event_details.number_of_seat) - int(Total_book_seat), 
                "total_earning": Total_event_eaning['total_earning'], 
                "event_city": Particular_event_details.event_address_city, 
                "event_state": Particular_event_details.event_address_state
            }
        }, status=200)
        
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=400)  
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_update_view(request, id): 
    try:

        if serializer.SerializerCreateEvent(data = request.data).is_valid():

            # Particular event object 
            Particular_event_object = Event_details.objects.get(id = id)
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
            Particular_event_object.organizer_name = request.data['organizer_name']
            Particular_event_object.organizer_contact_number = request.data['organizer_contact_number']
            Particular_event_object.number_of_seat = request.data['number_of_seat']
            Particular_event_object.is_vip_seat = request.data['is_vip_seat']
            Particular_event_object.event_address_city = request.data['event_city']
            Particular_event_object.event_address_state = request.data['event_state']
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
def event_gallery_view(request, id):
    try:

        Particular_event_gallery_list = Event_gallery.objects.filter(event_id = id, delete = False).order_by("-id")
        Particular_event_gallery_list_paginator = Paginator(Particular_event_gallery_list, int(request.query_params.get("page_size")))
        Particular_event_gallery_list_paginator_page = Particular_event_gallery_list_paginator.get_page(int(request.query_params.get("page_number")))
        Particular_event_gallery_list_paginator_page_data = serializer.EventGalleryListFetch(Particular_event_gallery_list_paginator_page, many = True)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": Particular_event_gallery_list_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": 'Network request failed'
        }, status=500)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_galleryupload_view(request, id): 
    try:
        if serializer.EventGalleryUploadSerializer(data = request.data).is_valid():

            event_gallery_bulk_insert = []
            for image in request.data['images']: 
                event_gallery_bulk_insert.append(
                    Event_gallery(
                        type = image['type'], 
                        link = image['image'], 
                        event_id = id, 
                        upload_by_id = request.user.id
                    )
                )
            
            Event_gallery.objects.bulk_create(event_gallery_bulk_insert)
            return Response({
                "status": True, 
                "message": "Upload"
            }, status=200) 
        else:
            return Response({
                "status": False,
                "message": 'Failed to upload'
            }, status=400)
    except Exception as e:
        return Response({
            "status": False, 
            "message": 'Network request failed'
        }, status=500)
    
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_gallerydelete_view(request, id):
    try:

        Event_gallery.objects.filter(id = id).update(delete = True)
        return Response({
            "status": True, 
            "message": "Delete"
        }, status=200) 
    except Exception as e:
        return Response({
            "status": False, 
            "message": 'Network request failed'
        }, status=500)



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def transaction_view(request): 
    try:

        # Fetch event transaction information 
        status = request.query_params.get("status")

        if status == "all":
            Transaction_list = Session.objects.filter(payment_status = "paid")
        else:
            Transaction_list = Session.objects.filter(metadata__contains={"type": str(status)}) 
        
        Transaction_list = Paginator(Transaction_list, int(request.query_params.get("page_size")))
        Transaction_list_paginator = Transaction_list.get_page(int(request.query_params.get("page_number")))
        Transaction_list_paginator_data = serializer.TransactionListDataFetch(Transaction_list_paginator, many = True)
        return Response({
            "status": True, 
            'message': "Fetch", 
            "data": Transaction_list_paginator_data.data
        }, status=200)
    except Exception as e:
        return Response({
            'status': False, 
            "message": "Network request failed"
        }, status=500)
        

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def user_list_view(request):
    try:

        User_list = User_details.objects.filter(is_admin = False).order_by("-id")
        User_list_paginator = Paginator(User_list, int(request.query_params.get("page_size")))
        User_list_paginator_page = User_list_paginator.get_page(int(request.query_params.get("page_number")))
        User_list_paginator_page_data = serializer.UserListDataFetch(User_list_paginator_page, many = True)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": User_list_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def user_details_view(request, id):
    try:
        Particular_user_object = User_details.objects.get(id = id)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": {
                "first_name": Particular_user_object.first_name, 
                "profession": Particular_user_object.profession, 
                "gender": Particular_user_object.gender, 
                "dob": Particular_user_object.dob, 
                "phone_number": Particular_user_object.mobile, 
                "email": Particular_user_object.email, 
                "address":  Particular_user_object.address, 
                "professional_description": Particular_user_object.profession_description, 
                "profile_image": Particular_user_object.profile_image
            }
        }, status=200)
    except Exception as e :
        return Response({
            "status": False,
            "message": "Network request failed"
        }, status=500)
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_qrscan_view(request):
    try:

        if serializer.EventQrScanSerializer(data = request.data).is_valid():
            ticket_information = User_event_model.objects.filter(ticket_number = request.data['ticket_number']).values("event__event_name", "event__event_image", "event__category__category_name", "id").first()
            return Response({
                "status": True,
                "message": "Fetch", 
                "data": ticket_information
            }, status=200)
        else:
            return Response({
                "status": False, 
                "message": "Failed to fetch ticket information "
            }, status=400)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_ticketdetails_view(request, id):
    try:

        Particular_ticket_details = User_event_model.objects.filter(id = id)
        Particular_ticket_details = serializer.ParticularEventDetailsFetch(Particular_ticket_details, many = True)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": Particular_ticket_details.data[0]
        }, status=200)
    except Exception as e: 
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def event_transaction_view(request, id): 
    try:

        Event_information = Event_details.objects.filter(id = id).values("event_image", "event_name", "event_address", "organizer_name").first() 
        Event_transaction = Session.objects.filter(metadata__contains={"event_id": str(id), "type": "event"}, payment_status= "paid")
        Event_transaction_paginator = Paginator(Event_transaction, int(request.query_params.get("page_size")))
        Event_transaction_paginator_page = Event_transaction_paginator.get_page(int(request.query_params.get("page_number")))
        Event_transaction_paginator_page_data = serializer.EventTransactionDetailsData(Event_transaction_paginator_page, many = True)

        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": {
                "event": Event_information, 
                "event_transaction": Event_transaction_paginator_page_data.data
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
def donation_create_view(request):
    try:

        if serializer.CreateDonationSerializer(data = request.data).is_valid():
            
            # Check donation name 
            check_donation_name = Donation_model.objects.filter(donation_name = request.data['donation_name']).count()

            if check_donation_name > 0:
                return Response({
                    "status": False, 
                    "message": "Already create donation with this name"
                }, status=400)
            else:
                New_donation = Donation_model.objects.create(
                    image = request.data['image'], 
                    donation_name = request.data['donation_name'], 
                    donation_target = request.data['donation_target'], 
                    donation_start_date = request.data['donation_start_date'], 
                    donation_end_date = request.data['donation_end_date'], 
                    location = request.data['location'], 
                    donation_address = request.data['donation_address'], 
                    description = request.data['description'], 
                    organizer_name = request.data['organizer_name'], 
                    organizer_contact = request.data['organizer_contact'], 
                    donation_create_by_id = request.user.id
                )
                return Response({
                    "status": True, 
                    "message": "Create"
                }, status=200)
        else:
            return Response({
                "status": False, 
                "message": "Failed to create donation"
            }, status=400)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def donation_list_view(request): 
    try:
        Donation_data = Donation_model.objects.all().order_by("-id")
        Donation_data_paginator = Paginator(Donation_data, int(request.query_params.get("page_number")))
        Donation_data_paginator_page = Donation_data_paginator.get_page(int(request.query_params.get("page_size")))
        Donation_data_paginator_page_data = serializer.DonationListDataFetch(Donation_data_paginator_page, many = True)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": Donation_data_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def donation_update_view(request, id): 
    try:
        return Response({
            "status": True, 
            "message": "Update"
        }, status=200) 
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def admin_upload_image(request):
    try:

        if serializer.UploadImageSerializer(data = request.data).is_valid():

            # new unique id
            unique_id = str(uuid.uuid4())

            file_name = request.FILES['image'].name 

            # Upload file name 
            update_file_name = f"{unique_id}.{str(file_name).split('.')[1]}"
            request.FILES['image'].name = update_file_name

            # upload new image 

            upload_new_image = Image(
                image = request.FILES["image"]
            )

            upload_new_image.save() 
            update_file_name = update_file_name.replace(" ", "_")

            return Response({
                "status": True, 
                "message": "Upload", 
                'image_url': f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/image/{update_file_name}"
            }, status=200)
        else:
            return Response({
                "status": False, 
                "message": "Failed to upload image"
            }, status=400)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)
    
