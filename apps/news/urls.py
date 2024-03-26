from django.urls import path
from apps.news import views

urlpatterns = [
    path("get", views.news_list_view, name="news_list"), 
    path("<int:id>", views.news_details_view, name="news_detailw")
]
