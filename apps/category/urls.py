from django.urls import path 
from apps.category import views

urlpatterns = [
    path("create", views.CreateCategory, name="create-category"), 
    path("update", views.UpdateCategory, name="update-category" ), 
    path("list", views.FetchCategory, name = "category-list")
]
