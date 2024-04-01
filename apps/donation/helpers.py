from apps.user.models import Donation as User_donation_model
from apps.donation.models import Details as Donation_details
from djstripe.models import Session 
import random

def generate_certification_number():
    return random.randint(10**11, (10**12)-1)

def check_user_donation_entry(user_id, donation_id, name_visible): 
    """
    Function information:
        Check user donation entry and if entry exists than 
    """
    try:
        User_donation_object = User_donation_model.objects.create(
            user_id = user_id, 
            donation_id = donation_id, 
            is_name_visible = name_visible, 
            transaction_status = "Pending", 
            certification_number = generate_certification_number() 
        )

        return True, User_donation_object.id
    except Exception as e:
        return False, None
    
def get_donation_member_information(donation_id):
    try:
        User_donation_member = User_donation_model.objects.filter(donation_id = donation_id).values("user_id").distinct().count()

        User_donation_member_info = User_donation_model.objects.filter(donation_id = donation_id).values("user__profile_image").distinct()
        return {
            "donated_user_count": User_donation_member, 
            "donated_member": User_donation_member_info
        }
    except Exception as e:
        return False