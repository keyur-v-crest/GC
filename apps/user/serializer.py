from rest_framework import serializers 
from apps.user.models import Details
from apps.user.models import Achievments as User_achievments
from apps.user.models import BannerImage

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

class AchivementListSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = User_achievments
        fields = ['id', "count", "user_details"]

    def get_user_details(self, object):
        try:
            return {
                "background_image": object.user.background_image,
                "profile_image": object.user.profile_image,
                "username": object.user.first_name, 
                "profession": object.user.profession, 
                "profession_description": object.user.profession_description
            }
        except Exception as e:
            return {}
        
class AchieverListSerializer(serializers.ModelSerializer): 
    user_details = serializers.SerializerMethodField()
    class Meta:
        model = User_achievments
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

class ProfileUpdateSerializer(serializers.Serializer):
    user_image = serializers.CharField(required = True)
    username = serializers.CharField(required= True)
    dob = serializers.CharField(required = True)
    email = serializers.CharField(required = True)
    gender = serializers.CharField(required = True)
    address = serializers.CharField(required = True)
    profession = serializers.CharField(required = True)
    linkdin = serializers.CharField(required = True, allow_null = True)
    upwork = serializers.CharField(required = True, allow_null = True)
    background_image = serializers.CharField(required = True, allow_null = True)
    achivements = serializers.ListField(required = True)

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required = True)
    current_password = serializers.CharField(required = True)

class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerImage
        fields = ["id", "image", "title", "subtitle"]