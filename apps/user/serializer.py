from rest_framework import serializers 

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