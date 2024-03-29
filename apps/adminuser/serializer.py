from rest_framework import serializers 
from apps.user.models import Details as User_details 
from apps.event.models import Details as Event_details 
from apps.event.models import Gallery as Event_gallery
from apps.news.models import Details as News_details
from djstripe.models import Session
from apps.user.models import Event as User_event
from apps.user.models import Donation as User_donation
from apps.user.models import Achievments as Achievment_model
from apps.donation.models import Details as Donation_details
from djstripe.models import WebhookEventTrigger
import json 

class SerializerCreateSuperUser(serializers.Serializer): 
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    is_superuser = serializers.BooleanField(required = True)

    
class SerializerUserLogin(serializers.Serializer): 
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    is_superadmin = serializers.BooleanField(required = True)


class SerializersUserFetch(serializers.ModelSerializer): 
    class Meta: 
        model = User_details
        fields = ['email', 'is_superuser', 'created_at', 'updated_at']

class SerializerCreateEvent(serializers.Serializer):
    event_name = serializers.CharField(required = True)
    event_description = serializers.CharField(required = True)
    price = serializers.FloatField(required = True)
    category = serializers.IntegerField(required = True)
    event_date = serializers.DateField(required = True)
    publish_date = serializers.DateField(required = True)
    event_start_time = serializers.CharField(required = True)
    event_end_time =  serializers.CharField(required= True)
    event_address = serializers.CharField(required = True)
    event_address_latitude = serializers.CharField(required = True)
    event_address_longitude = serializers.CharField(required = True)
    event_image = serializers.CharField(required = True)
    number_of_seat = serializers.IntegerField(required = True)
    is_vip_seat = serializers.BooleanField(required = True)
    event_city = serializers.CharField(required = True)
    event_state = serializers.CharField(required = True)
    organizer_name = serializers.CharField(required = True)
    organizer_contact_number = serializers.CharField(required = True)
    organizer_image = serializers.CharField(required = True)

class SerializerUpdateEvent(serializers.Serializer): 
    id = serializers.IntegerField(required = True)
    event_name = serializers.CharField(required = True)
    event_description = serializers.CharField(required = True)
    price = serializers.FloatField(required = True)
    category = serializers.IntegerField(required = True)
    event_date = serializers.DateField(required = True)
    publish_date = serializers.DateField(required = True)
    event_start_time = serializers.CharField(required = True)
    event_end_time =  serializers.CharField(required= True)
    event_address = serializers.CharField(required = True)
    event_address_latitude = serializers.CharField(required = True)
    event_address_longitude = serializers.CharField(required = True)
    event_image = serializers.CharField(required = True)
    number_of_people = serializers.IntegerField(required = True)
    number_of_seat = serializers.IntegerField(required = True)
    organizer_name = serializers.CharField(required = True)
    organizer_contact_number = serializers.CharField(required = True)
    organizer_description = serializers.CharField(required = True) 
    organizer_image = serializers.CharField(required = True, allow_null = True, allow_blank = True)
    event_type = serializers.BooleanField(required = True)

class SerializerPaginator(serializers.Serializer):
    page_number = serializers.IntegerField(required = True)
    page_size = serializers.IntegerField(required = True) 


class SerializerFetchEventList(serializers.ModelSerializer):

    category_image = serializers.SerializerMethodField()

    class Meta: 
        model = Event_details 
        fields = ['id', "category_image", "event_image", "event_date", "event_start_time", "event_name", "event_description", "event_address", "event_address_latitude", "event_address_longitude", "price"]

    def get_category_image(self, obj):
        return obj.category.category_image

class TransactionListDataFetch(serializers.ModelSerializer): 
    event_details = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ['id', "amount_total", "djstripe_created", "djstripe_updated", "event_details"]
    
    def get_event_details(self, object): 
        metadata = object.metadata

        try: 
            if metadata['type'] == "event": 
                event_id = metadata['event_id']
                event_details_object = Event_details.objects.filter(id = event_id).values("event_image", "event_name", "id").first()
                return event_details_object
            else:
                return {}
        except Exception as e:
            return {}
        
class UserListDataFetch(serializers.ModelSerializer): 
    class Meta:
        model = User_details
        fields = ["id", "profile_image", "profession", "first_name", "last_name", "account_status", "created_at", "updated_at"]

class EventQrScanSerializer(serializers.Serializer): 
    ticket_number = serializers.CharField(required = True)

class TicketEventDetails(serializers.ModelSerializer):
    class Meta:
        model = Event_details
        fields = ["id", "event_name", "event_date"]

class ParticularEventDetailsFetch(serializers.ModelSerializer):
    event = TicketEventDetails(read_only = True) 
    book_by_username = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField() 
    number_of_seat = serializers.SerializerMethodField()

    class Meta:
        model = User_event 
        fields = ["id", "ticket_number", "event", "book_by_username", "payment", "number_of_seat"]
    
    def get_book_by_username(self, object): 
        return {
            "username": object.book_by.first_name, 
            "mobilenbumber": object.book_by.mobile
        }
    
    def get_payment(self, object): 
        Event_data = WebhookEventTrigger.objects.filter(id = object.payment_id).values("body").first()
        Event_metadata = json.loads(Event_data['body'])
        return {
                "paid_amount": Event_metadata['data']['object']['amount_total'], 
                "payment_type": Event_metadata['data']['object']['payment_method_types'], 
                "payment_status": Event_metadata['data']['object']['status']
            }

    def get_number_of_seat(self, object): 
        Number_of_seat_count = User_event.objects.filter(payment_id = object.payment_id, transaction_status = "Complete").count()
        return Number_of_seat_count        
    
class EventTransactionDetailsData(serializers.ModelSerializer): 
    transaction_username = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ['id', "payment_method_types", "amount_total", "djstripe_created", "djstripe_updated", "transaction_username"]
    
    def get_transaction_username(self, object): 
        client_reference_id = object.client_reference_id
        User_data = User_details.objects.filter(id = client_reference_id).values("profile_image", "first_name").first()
        return User_data
    
class CreateDonationSerializer(serializers.Serializer): 
    donation_name = serializers.CharField(required = True)
    category = serializers.IntegerField(required = True)
    donation_target = serializers.FloatField(required = True) 
    image = serializers.CharField(required = True)
    donation_start_date = serializers.CharField(required = True)
    donation_end_date = serializers.CharField(required = True)
    donation_address = serializers.CharField(required = True)
    donation_city = serializers.CharField(required = True)
    donation_state = serializers.CharField(required = True)
    description = serializers.CharField(required = True)
    organizer_name = serializers.CharField(required = True)
    organizer_contact = serializers.CharField(required  = True)
    

class DonationListDataFetch(serializers.ModelSerializer): 
    raise_amount = serializers.SerializerMethodField()
    last_transaction = serializers.SerializerMethodField()
    class Meta:
        model = Donation_details 
        fields = ["id", "donation_name", "image", "image", "donation_address", "donation_target", "organizer_name", "created_at", "updated_at", 
            "organizer_image", "donation_city", "raise_amount", "last_transaction"]

    def get_raise_amount(self, object): 
        try:
            Total_amount = Session.objects.filter(metadata__contains={"donation_id": str(object.id)}, payment_status = "paid").aggregate(total_amount = Sum("amount_total"))
            return Total_amount
        except Exception as e:
            return 0
    
    def get_last_transaction(self, object): 
        try:
            Donation_last_transaction = Session.objects.filter(metadata__contains= {"donation_id": str(object.id)}, payment_status="paid").values("djstripe_updated").order_by("-id").first()
            return Donation_last_transaction
        except Exception as e:
            return None
        
class UploadImageSerializer(serializers.Serializer):
    image = serializers.FileField(required = True)
    # type = serializers.CharField(required = True)

class EventGalleryListFetch(serializers.ModelSerializer): 
    class Meta:
        model = Event_gallery
        fields = ["id", "link", "type"]

class EventGalleryUploadSerializer(serializers.Serializer):
    images = serializers.ListField(required = True)

class EventSelectionList(serializers.ModelSerializer):
    class Meta:
        model = Event_details
        fields = ['id', "event_name"]

class UserAccountUpdateSerializer(serializers.Serializer): 
    status = serializers.CharField(required = True)

class NewsCreateSerializer(serializers.Serializer): 
    image = serializers.CharField(required = True)
    name = serializers.CharField(required = True)
    news_type = serializers.CharField(required = True)
    short_description = serializers.CharField(required = True)
    publish_date = serializers.CharField(required = True)
    description = serializers.CharField(required = True)

class NewsListFetch(serializers.ModelSerializer): 
    class Meta:
        model = News_details
        fields = ["id", "name", "short_description", "count", "image"]

class DonationTransactionListSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    transaction_info = serializers.SerializerMethodField()
    class Meta:
        model = User_donation
        fields = ["id", "user_info", "transaction_info", "created_at", "updated_at", "is_name_visible"]

    def get_user_info(self, object): 
        try:
            return {
                "username": object.user.first_name,
                "profile_image": object.user.profile_image
            }
        except Exception as e:
            return {}
    
    def get_transaction_info(self, object):
        try:
            Transaction_data = object.payment.body
            Transaction_data = json.loads(Transaction_data)
            return {
                "transaction_amount": Transaction_data['data']['object']['amount_total'], 
                "payment_method": Transaction_data['data']['object']['payment_method_types']
            }
        except Exception as e:
            return {}


class AchieverListSerializer(serializers.ModelSerializer): 
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = Achievment_model
        fields = ["id", "count", "user_details"]
    
    def get_user_details(self, object):
        try:
            return {
                "user_image": object.user.profile_image,
                "username": object.user.first_name, 
                "linkdin": object.user.linkdin, 
                "upwork": object.user.upwork, 
                "profession": object.user.profession
            }
        except Exception as e:
            return {}