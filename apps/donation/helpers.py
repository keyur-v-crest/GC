from apps.user.models import Donation as User_donation_model

def check_user_donation_entry(user_id, donation_id, name_visible): 
    """
    Function information:
        Check user donation entry and if entry exists than 
    """
    try:
        
        User_donation_check = User_donation_model.objects.filter(user_id = user_id, donation_id = donation_id, transaction_status = "Pending").count()

        if User_donation_check == 0:
            User_donation_model.objects.create(
                user_id = user_id, 
                donation_id = donation_id, 
                is_name_visible = name_visible, 
                transaction_status = "Pending"
            )

        return True
    except Exception as e:
        return False