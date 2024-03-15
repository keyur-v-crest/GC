from rest_framework import serializers
from apps.event.models import Details 

class SerializerEventDetails(serializers.ModelSerializer):
    category_info = serializers.SerializerMethodField()
    class Meta:
        model = Details 
        fields = ['id', 'event_name', 'event_date', 'event_start_time', 'event_description', 'price', 'event_address', 'event_address_latitude', 'event_address_longitude', 'category_info']

    def get_category_info(self, object): 
        return object.category.category_image
    
class SerializerParticularEventDetails(serializers.Serializer): 
    id = serializers.IntegerField(required = True)

class SerializerEventPayment(serializers.Serializer): 
    family_member = serializers.ListField(required = True)
    event_id = serializers.IntegerField(required = True)
    event_type = serializers.BooleanField(required = True)
    event_name = serializers.CharField(required = True)
    event_price = serializers.IntegerField(required = True)
    booking_count = serializers.IntegerField(required = True)

class event_history_serializer(serializers.Serializer):
    status = serializers.CharField(required = True)
    page_number = serializers.IntegerField(required = True)
    page_size = serializers.IntegerField(required = True)