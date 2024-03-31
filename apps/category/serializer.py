from rest_framework import serializers 
from apps.category.models import Details as Category_details

class CreateCategorySerializer(serializers.Serializer): 
    name = serializers.CharField(required = True)
    image = serializers.CharField(required = True)
    type = serializers.CharField(required = True)
    is_active = serializers.BooleanField(required = True)

class UpdateCategorySerializer(serializers.Serializer): 
    id = serializers.IntegerField(required = True)
    name = serializers.CharField(required = True)
    image = serializers.CharField(required = True)

class FetchCategoryList(serializers.ModelSerializer):
    class Meta: 
        model = Category_details
        fields = ['category_name', 'category_image', 'created_at', 'id']