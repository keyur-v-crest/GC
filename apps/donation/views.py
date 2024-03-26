from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response
from apps.donation.models import Details as Donation_details 
from datetime import datetime

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def donation_list_view(request):
    try:
        today_date = datetime.today()
        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        Donation_list = Donation_details.objects.filter(donation_end_date__gte=today_date, donation_start_date__lte=today_date).order_by("-id")
        print(Donation_list)
        return Response({
            "status": True,
            "message": "Fetch"
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message": "Network request failed"
        }, status=500)