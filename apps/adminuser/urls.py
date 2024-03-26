from django.urls import path 
from apps.adminuser import views

urlpatterns = [
    path("login", views.RouteAdminLogin, name="super-admin-login"), 
    path("check", views.admin_check_view, name="Admin_token_check"), 

    # User related CRUD 
    path("user", views.user_list_view, name="user_list_view"),  
    path("verifiedUser", views.user_verifiedlist_view, name="user_verified_view"), 
    path("user/<int:id>/account", views.user_accountupdate_view, name="user_verified_view"), 
    path("user/<int:id>", views.user_details_view, name="user_details_view"), 

    # Event related CRUD
    path("event/create", views.event_create_view, name="event_create"), 
    path("event", views.event_list_view, name="event_list"), 
    path("event/<int:id>", views.event_details_view, name="event_details"), 
    path("event/update/<int:id>", views.event_update_view, name="event_update"),

    # EventGallery related CRUD
    path("event/gallery/<int:id>", views.event_gallery_view, name="event_gallery"), 
    path("event/gallery/delete/<int:id>", views.event_gallerydelete_view, name="event_gallery_delete"), 
    path("event/gallery/upload/<int:id>", views.event_galleryupload_view, name="event_gallery_upload"), 

    # Donation related CRUD
    path("donation/create", views.donation_create_view, name="donation_create"), 
    path("donation", views.donation_list_view, name="donation_list"), 
    path("donation/<int:id>", views.donation_details_view, name="donation_details"), 
    path("donation/update/<int:id>", views.donation_update_view, name="donation_details"), 

    path("event/qrscan", views.event_qrscan_view, name="event_qr_scan"), 
    path("event/ticket/<int:id>", views.event_ticketdetails_view, name="event_ticketdetails_view"), 
    path("event/transaction/<int:id>", views.event_transaction_view, name="event_transaction_view"), 
    path("event/selection", views.event_selection_view, name = "event_selection"), 

    # Transaction view
    path("transaction", views.transaction_view, name="transaction_view"), 
    path("uploadImage", views.admin_upload_image, name="admin_upload_image")
    
]
