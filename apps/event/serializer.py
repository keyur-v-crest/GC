from rest_framework import serializers
from apps.event.models import Details 
from apps.user.models import Event as User_event
from apps.event.models import Gallery
from djstripe.models import WebhookEventTrigger

class SerializerEventDetails(serializers.ModelSerializer):
    category_info = serializers.SerializerMethodField()
    class Meta:
        model = Details 
        fields = ['id', 'event_name', 'event_date', 'event_start_time', 'event_description', 'price', 'event_address', 'event_address_latitude', 
                'event_address_longitude', 'category_info', "event_address_city", "event_address_state", "event_image"]

    def get_category_info(self, object): 
        return object.category.category_image
    
class SerializerParticularEventDetails(serializers.Serializer): 
    id = serializers.IntegerField(required = True)

class SerializerEventPayment(serializers.Serializer): 
    family_member = serializers.ListField(required = True)
    event_id = serializers.IntegerField(required = True)
    event_type = serializers.CharField(required = True)
    event_name = serializers.CharField(required = True)
    event_price = serializers.IntegerField(required = True)
    booking_count = serializers.IntegerField(required = True)

class event_history_serializer(serializers.Serializer):
    status = serializers.CharField(required = True)
    page_number = serializers.IntegerField(required = True)
    page_size = serializers.IntegerField(required = True)

class PaymentDetails(serializers.ModelSerializer): 
    class Meta:
        model = WebhookEventTrigger
        fields = [""]

class EventDetails(serializers.ModelSerializer):
    category_image = serializers.SerializerMethodField()
    class Meta:
        model = Details
        fields = ["id", "event_image", "event_name", "event_description", "organizer_name", "price", "event_address", "event_address_latitude", "event_address_longitude", 
        "event_date", "event_start_time", "event_end_time", "category_image"]

    def get_category_image(self, object): 
        try:
            return object.category.category_image
        except Exception as e:
            return None

class UserEventListFechSerializer(serializers.ModelSerializer):
    event = EventDetails(read_only = True)
    class Meta:
        model = User_event
        fields = ["id", "created_at", "updated_at", "transaction_status", "status", "ticket_number", "event"]

class EventDateWiseSerializer(serializers.Serializer): 
    year = serializers.IntegerField(required = True)
    month = serializers.IntegerField(required = True)

class EventDateWiseData(serializers.ModelSerializer):
    event = EventDetails(read_only = True)
    class Meta:
        model = User_event
        fields = ['id', "event"]

class EventImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "type", "link"]

class EventFilterDataSerializer(serializers.ModelSerializer):
    event = EventDetails(read_only = True)
    class Meta:
        model = User_event
        fields = ["id", "event"]

class TickerEventDetails(serializers.ModelSerializer): 
    class Meta:
        model = Details
        fields = ['id', "event_image", "event_name", "event_date", "organizer_name"]

class EventTicketDataSerializer(serializers.ModelSerializer): 
    event = TickerEventDetails(read_only = True)
    class Meta: 
        model = User_event
        fields = ["id", "event", "ticket_number"]

class EventGalleryListSerializer(serializers.ModelSerializer): 
    event = EventDetails(read_only = True)
    class Meta:
        model = User_event
        fields = ["id", "event"]

class EventImageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Gallery 
        fields = ["id", "link", "type"]