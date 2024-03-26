from rest_framework import serializers 
from apps.donation.models import Details as Donation_details
from apps.user.models import Donation as User_donation
from djstripe.models import Session
from django.db.models import Sum

class DonationListSerializer(serializers.ModelSerializer):
    raise_amount = serializers.SerializerMethodField()
    last_transaction = serializers.SerializerMethodField()
    class Meta:
        model = Donation_details
        fields = ["id", "image", "organizer_image", "organizer_name", "donation_name", "donation_target", "raise_amount", "last_transaction"]

    def get_raise_amount(self, object): 
        try:
            Total_amount = Session.objects.filter(metadata__contains={"donation_id": str(object.id)}, payment_status = "paid").aggregate(total_amount = Sum("amount_total"))
            return Total_amount
        except Exception as e:
            return 0
    
    def get_last_transaction(self, object): 
        try:
            Donation_last_transaction = Session.objects.filter(metadata__contains= {"donation_id": str(object.id)}, payment_status="paid").values("djstripe_updated").order_by("-id").first()
            return Donation_last_transaction
        except Exception as e:
            return None
class DonationPaymentSerializer(serializers.Serializer):
    donation_id = serializers.IntegerField(required = True)
    amount = serializers.FloatField(required = True)
    donation_name = serializers.CharField(required = True)
    is_name_visible = serializers.BooleanField(required = True)


class DonationTransactionList(serializers.ModelSerializer):
    donation_details = serializers.SerializerMethodField()
    class Meta:
        model = User_donation
        fields = ["id", "transaction_status", "donation_details", "created_at", "updated_at"]

    def get_donation_details(self, object):
        try:
            return {
                "donation_name": object.donation.donation_name,
                "donation_image": object.donation.image
            }
        except Exception as e:
            return {}