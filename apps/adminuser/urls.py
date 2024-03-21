from django.urls import path 
from apps.adminuser import views

urlpatterns = [
    
    # Transaction view
    path("transaction", views.transaction_view, name="transaction_view"), 

    path("create", views.RouteCreateSuperUser, name="create-super-admin"), 
    path("login", views.RouteAdminLogin, name="super-admin-login"), 
    path("get", views.RouteGetAllAdmin, name="super-admin-fetch"),

    # User related route 
    path("user", views.user_list_view, name="user_list_view"),  
    path("user/<int:id>", views.user_details_view, name="user_details_view"), 

    # Event related route
    path("event/create", views.RouteCreateEvent, name="create-event"), 
    path("event/get", views.RouteGetEventDetails, name="event-list"), 
    path("event/id", views.RouteGetParticularEventDetails, name="particular-event-details"), 
    path("event/update", views.RouteUpdateEventDetails, name="update-event-details"), 
    path("event/qrscan", views.event_qrscan_view, name="event_qr_scan"), 
    path("event/ticket/<int:id>", views.event_ticketdetails_view, name="event_ticketdetails_view")
]
