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
    path("event/delete/<int:id>", views.event_delete_view, name="event_delete"), 

    # EventGallery related CRUD
    path("event/gallery/<int:id>", views.event_gallery_view, name="event_gallery"), 
    path("event/gallery/delete/<int:id>", views.event_gallerydelete_view, name="event_gallery_delete"), 
    path("event/gallery/upload/<int:id>", views.event_galleryupload_view, name="event_gallery_upload"), 

    # Donation related CRUD
    path("donation/create", views.donation_create_view, name="donation_create"), 
    path("donation", views.donation_list_view, name="donation_list"), 
    path("donation/<int:id>", views.donation_details_view, name="donation_details"), 
    path("donation/update/<int:id>", views.donation_update_view, name="donation_details"), 
    path("donation/delete/<int:id>", views.donation_delete_view, name="donation_details"), 
    path("donation/transaction/<int:id>", views.donation_transaction_view, name="donation_transaction"), 
    path("donation/transactionList/<int:id>", views.donation_transactionlist_view, name="donation_transction_list"), 

    path("event/qrscan", views.event_qrscan_view, name="event_qr_scan"), 
    path("event/ticket/<int:id>", views.event_ticketdetails_view, name="event_ticketdetails_view"), 
    path("event/transaction/<int:id>", views.event_transaction_view, name="event_transaction_view"), 
    path("event/selection", views.event_selection_view, name = "event_selection"), 

    # Transaction view
    path("transaction", views.transaction_view, name="transaction_view"), 
    path("uploadImage", views.admin_upload_image, name="admin_upload_image"), 

    # Dashboard related CRUD 
    path("dashboard", views.dashboard_count_view, name="dashboard_count_view"), 

    # News related CRUD
    path("news/create", views.news_create_view, name="news_create"), 
    path("news/<int:id>", views.news_details_view, name="news_details"), 
    path("news/update/<int:id>", views.news_update_view, name="news_update"), 
    path("news/delete/<int:id>", views.news_delete_view, name="news_delete"), 
    path("news", views.news_list_view, name="news_list"), 

    # Profession related CRUD
    path("professional", views.professional_list_view, name="professional_list")
]
