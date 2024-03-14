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