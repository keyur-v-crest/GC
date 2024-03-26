from django.urls import path
from apps.donation import views

urlpatterns = [
    path("get", views.donation_list_view, name="donation_list"), 
    path("<int:id>", views.donation_details_view, name="donation_details"), 
    path("payment", views.donation_payment_view, name="donation_payment")
]
