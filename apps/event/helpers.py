from apps.event.models import Details as Event_details 
from apps.user.models import Event as User_event 
from djstripe.models import Session

def helper_check_number_of_seat(event_id, required_booking): 
    Allowed_booking_count = Event_details.objects.filter(id = event_id).values("number_of_seat").first()
    Allowed_booking_count = Allowed_booking_count['number_of_seat']
    Book_event_count = Session.objects.filter(metadata__contains={"event_id": str(event_id)}, payment_status = "paid").count()

    if Allowed_booking_count > (Book_event_count + required_booking):
        return True
    else:
        return False

def helper_user_event_status_check(event_id , user_id):
    """
    Helper:
        Check particular user already booked this event or not 
    """

    try:
        user_event_check = User_event.objects.get(event_id = event_id, user_id = user_id)
        user_event_book_id = user_event_check.book_by_id
        
        event_payment_status_check = Session.objects.filter(metadata__contains={"event_id": str(event_id)}, payment_status = "paid", client_reference_id = user_event_book_id).count()
    
        if event_payment_status_check > 0 :
            return False
        else:
            return True

    except Exception as e: 
        return True