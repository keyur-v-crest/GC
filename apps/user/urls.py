from django.urls import path 
from apps.user import views

urlpatterns = [
    
    # Step1
    path("userSignupStep1", views.RouteUserSignStep1), 
    
    # Step2
    path("mobileOtpSend", views.user_mobileverificationcode_send_route), 
    path("mobileVerify", views.user_mobileverify_view), 

    # Step3
    path("emailOtpSend", views.user_emailverificationcode_send_route), 
    path("emailVerify", views.user_emailverify_view), 

    # Step4
    path("userSignupStep4", views.RouteUserSignupStep2), 
    
    # Add member 
    path("addMember", views.user_familymember_add_view), 
    path("step3Complete", views.user_step3complete_view), 
    
    path("userSignupStep5", views.user_profileimage_view), 
    path("login", views.RouteUserLogin), 
    path("achievment/create", views.achievment_create_view), 
    path("achievment", views.achievment_list_view), 

    # Member
    path("familyMember", views.RouteFetchFamilyMembers), 
    path("member/<int:id>", views.particular_member_view), 
    path("member/update/<int:id>", views.particular_member_update_view), 

    path("screen/achievment", views.achivement_screen_list_view),
    path("screen/achievers", views.achiever_list_view),  
    path("screen/achievment/<int:id>", views.achivement_details_view), 

    # User profile CRUD
    path("profile", views.user_profiledetails_view), 
    path("profile/update", views.user_profile_update_view), 

    # Change password CRUD
    path("changepassword", views.user_changepassword_view), 

    # Banner image
    path("banner", views.user_banner_image), 

    # Account status 
    path("accountStatus", views.user_accountstatus_view), 

    # Forgetpassword related route
    path("check", views.user_check_view), 
    path("updatepassword", views.user_forgetpassword_view)
]
