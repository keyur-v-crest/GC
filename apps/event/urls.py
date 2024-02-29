from django.urls import path 
from apps.event import views

urlpatterns = [
    path("fetch", views.RouteFetchEvent, name="fetch-event-list"),
    path("payment", views.RouteEventPayment, name="make-event-payment")
]
