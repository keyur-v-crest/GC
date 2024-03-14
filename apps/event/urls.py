from django.urls import path 
from apps.event import views

urlpatterns = [
    path("fetch", views.RouteFetchEvent, name="fetch-event-list"),
    path("eventById", views.GetEventByIdRoute, name="particular-event-information"), 
    path("payment", views.RouteEventPayment, name="make-event-payment")
]
