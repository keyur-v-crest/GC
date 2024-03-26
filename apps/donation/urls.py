from django.urls import path
from apps.donation import views

urlpatterns = [
    path("/get", views.donation_list_view, name="donation_list_view")
]
