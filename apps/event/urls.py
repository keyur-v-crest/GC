from django.urls import path 
from apps.event import views

urlpatterns = [
    path("list", views.event_list_view, name="event_list_view"),
    path("<int:id>", views.event_details_view, name="event_details_view"), 
    path("payment", views.event_payment_view, name="event_payment_view"),
    path("history", views.event_history_view, name="event_history_view"), 
    path("calendar", views.event_date_view, name="event_datewise")
]
