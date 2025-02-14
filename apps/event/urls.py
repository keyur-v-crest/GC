from django.urls import path 
from apps.event import views

urlpatterns = [
    path("upcoming", views.event_upcominglist_view, name="event_upcoming"),
    path("featured", views.event_featuredlist_view, name="event_featured"), 
    path("<int:id>", views.event_details_view, name="event_details"), 
    path("payment", views.event_payment_view, name="event_payment_view"),
    path("ticket/<int:id>", views.event_ticketdetails_view, name="event_ticketdetails"), 
    path("bookingHistory", views.event_history_view, name="event_history"), 
    path("history", views.event_historylist_view, name="event_history"), 

    # Event gallery CRUD
    path("gallery/recent", views.event_recentgallery_view, name="event_recentgallery"), 
    path("gallery/others", views.event_otheralubms_view, name="event_otheralumbmsview"),  
    path("gallery/<int:id>", views.event_imagefile_view, name="event_imagefile"), 
    
    path("calendar", views.event_date_view, name="event_datewise"), 
    path("particularDate", views.event_particulardate_view, name="event_particulardate"), 
    path("gallery/<int:id>", views.event_gallery_view, name="event_gallery"),
    path("filter", views.event_filter_view, name="event_filter_view"), 
    path("ticket", views.event_ticketlist_view, name="event_ticket_view")

]
