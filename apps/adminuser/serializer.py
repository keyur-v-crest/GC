from rest_framework import serializers 
from apps.user.models import Details as User_details 
from apps.event.models import Details as Event_details 
from djstripe.models import Session

class SerializerCreateSuperUser(serializers.Serializer): 
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    is_superuser = serializers.BooleanField(required = True)

    
class SerializerUserLogin(serializers.Serializer): 
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)


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
    event_gallery = serializers.ListField(required = True)
    number_of_people = serializers.IntegerField(required = True)
    number_of_seat = serializers.IntegerField(required = True)
    organizer_name = serializers.CharField(required = True)
    organizer_contact_number = serializers.CharField(required = True)
    organizer_description = serializers.CharField(required = True)
    organizer_image = serializers.CharField(required = True, allow_blank = True, allow_null = True)
    event_type = serializers.BooleanField(required = True)

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

class SerializersFetchParticularEventDetails(serializers.Serializer): 
    id = serializers.IntegerField(required = True)

class SerializerFetchEventList(serializers.ModelSerializer):

    category_name = serializers.SerializerMethodField()

    class Meta: 
        model = Event_details 
        fields = ['id', "category_name", "event_image", "event_date", "event_start_time", "event_name", "event_description", "event_address", "event_address_latitude", "event_address_longitude"]

    def get_category_name(self, obj):
        return obj.category.category_name

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