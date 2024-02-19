from django.urls import path 
from apps.user import views

urlpatterns = [
    path("userSignupStep1", views.RouteUserSignStep1)
]
