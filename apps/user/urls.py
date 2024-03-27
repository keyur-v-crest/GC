from django.urls import path 
from apps.user import views

urlpatterns = [
    path("userSignupStep1", views.RouteUserSignStep1), 
    path("userSignupStep2", views.RouteUserSignupStep2), 
    path("userSignupStep3", views.RouteUserSignupStep3), 
    path("userSignupStep4", views.RotueUserSignupStep4), 
    path("login", views.RouteUserLogin), 
    path("familyMember", views.RouteFetchFamilyMembers), 
    path("achievment/create", views.achievment_create_view), 
    path("achievment", views.achievment_list_view), 

    path("screen/achievment", views.achivement_screen_list_view),
    path("screen/achievers", views.achiever_list_view),  
    path("screen/achievment/<int:id>", views.achivement_details_view), 

    # User profile CRUD
    path("profile", views.user_profiiledetails_view), 
    path("profile/update", views.user_profile_update_view), 

    # Change password CRUD
    path("changepassword", views.user_changepassword_view)
]
