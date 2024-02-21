from django.urls import path 
from apps.adminuser import views

urlpatterns = [
    path("create", views.RouteCreateSuperUser, name="create-super-admin"), 
    path("login", views.RouteAdminLogin, name="super-admin-login"), 
    path("get", views.RouteGetAllAdmin, name="super-admin-fetch")
]
