from rest_framework import serializers 
from apps.user.models import Details as User_details 
from apps.event.models import Details as Event_details 

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
    number_of_people = serializers.IntegerField(required = True)
    organizer_name = serializers.CharField(required = True)
    organizer_contact_number = serializers.CharField(required = True)
    organizer_description = serializers.CharField(required = True)

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
    organizer_name = serializers.CharField(required = True)
    organizer_contact_number = serializers.CharField(required = True)
    organizer_description = serializers.CharField(required = True)
    

class SerializerPaginator(serializers.Serializer):
    page_number = serializers.IntegerField(required = True)
    page_size = serializers.IntegerField(required = True) 

class SerializersFetchParticularEventDetails(serializers.Serializer): 
    id = serializers.IntegerField(required = True)

class SerializerFetchEventList(serializers.ModelSerializer):

    category_name = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta: 
        model = Event_details 
        fields = '__all__'

    def get_category_name(self, obj):
        return obj.category.category_name

    def get_created_by(self, obj):
        # Add your logic here to calculate the value for extra_column_2
        return obj.event_create_by.email