from django.urls import path 
from apps.adminuser import views

urlpatterns = [
    path("login", views.RouteAdminLogin, name="super-admin-login"), 
    path("check", views.admin_check_view, name="Admin_token_check"), 

    # User related route 
    path("user", views.user_list_view, name="user_list_view"),  
    path("user/<int:id>", views.user_details_view, name="user_details_view"), 

    # Event related route
    path("event/create", views.RouteCreateEvent, name="create-event"), 
    path("event/get", views.RouteGetEventDetails, name="event-list"), 
    path("event/id", views.RouteGetParticularEventDetails, name="particular-event-details"), 
    path("event/update", views.RouteUpdateEventDetails, name="update-event-details"), 
    path("event/qrscan", views.event_qrscan_view, name="event_qr_scan"), 
    path("event/ticket/<int:id>", views.event_ticketdetails_view, name="event_ticketdetails_view"), 
    path("event/transaction/<int:id>", views.event_transaction_view, name="event_transaction_view"), 
    # Transaction view
    path("transaction", views.transaction_view, name="transaction_view"), 

    path("donation/create", views.donation_create_view, name="donation_create"), 
    path("donation", views.donation_list_view, name="donation_list")
    
]
