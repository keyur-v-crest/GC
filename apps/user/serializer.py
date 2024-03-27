from rest_framework import serializers 
from apps.user.models import Details

class SerializerCreateUserStep1(serializers.Serializer):
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)
    email = serializers.CharField(required =True)
    password = serializers.CharField(required = True)
    mobile_number = serializers.CharField(required = True)
    dob = serializers.CharField(required = True)
    address = serializers.CharField(required = True) 
    profession = serializers.CharField(required = True)
    description = serializers.CharField(required = True)

class SerializersCreateUserStep2(serializers.Serializer): 
    gender = serializers.CharField(required = True)

class SerializersCreateUserStep3(serializers.Serializer): 
    first_name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True) 
    relation = serializers.CharField(required = True)
    email = serializers.CharField(required = True)
    mobile_number = serializers.CharField(required = True) 
    profession = serializers.CharField(required = True)
    description = serializers.CharField(required = True) 
    address = serializers.CharField(required = True) 

class SerializersCreateUserStep4(serializers.Serializer): 
    profile_image = serializers.CharField(required = True)


class SerializerUserLogin(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True) 
    
class SerializerFetchFamilyMemberInfo(serializers.ModelSerializer): 
    class Meta:
        model = Details
        fields = ['id', 'email', 'first_name']

class AcheivementCreateSerializer(serializers.Serializer):
    name = serializers.ListField(required = True)