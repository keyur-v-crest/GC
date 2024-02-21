from django.urls import path 
from apps.user import views

urlpatterns = [
    path("userSignupStep1", views.RouteUserSignStep1), 
    path("userSignupStep2", views.RouteUserSignupStep2), 
    path("userSignupStep3", views.RouteUserSignupStep3), 
    path("userSignupStep4", views.RotueUserSignupStep4), 
    path("login", views.RouteUserLogin), 
    path("familyMember", views.RouteFetchFamilyMembers)

]
