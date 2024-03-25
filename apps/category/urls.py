from django.urls import path 
from apps.category import views

urlpatterns = [
    path("create", views.category_create_view, name="category_create"),
    path("<int:id>", views.category_details_view, name="category_details"),  
    path("list", views.category_list_view, name = "category_list"), 
    path("update/<int:id>", views.category_update_view, name="category_update" ), 
    path("selection", views.category_selection_view, name="category_selection")
]
