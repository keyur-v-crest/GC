from rest_framework import serializers 
from apps.donation.models import Details as Donation_details

class DonationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_details
        fields = ["id", "image", "organizer_image", "organizer_name", "donation_name", "donation_target"]

class DonationPaymentSerializer(serializers.Serializer):
    donation_id = serializers.IntegerField(required = True)
    amount = serializers.FloatField(required = True)
    donation_name = serializers.CharField(required = True)
    is_name_visible = serializers.BooleanField(required = True)
