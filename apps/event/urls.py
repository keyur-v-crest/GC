from django.urls import path 
from apps.event import views

urlpatterns = [
    path("fetch", views.RouteFetchEvent, name="fetch-event-list")
]
