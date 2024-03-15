from django.urls import path 
from apps.event import views

urlpatterns = [
    path("list", views.event_list_view, name="event_list_view"),
    path("details", views.event_details_view, name="event_details_view"), 
    path("payment", views.event_payment_view, name="event_payment_view")
]
