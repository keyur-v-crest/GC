from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from apps.user.helpers import CheckUserAuthentication
from rest_framework.response import Response 
from apps.news.models import Details as News_model 
from django.core.paginator import Paginator, EmptyPage
from apps.news import serializer
from datetime import datetime

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def news_list_view(request):
    try:
        today_date = datetime.today()
        type = request.query_params.get("type")
        page_number = int(request.query_params.get("page_number"))
        page_size = int(request.query_params.get("page_size"))

        New_list = News_model.objects.filter(news_type = type, publish_date__lte=today_date).order_by("-id")
        New_list_paginator = Paginator(New_list, page_size)
        
        try:
            New_list_paginator_page = New_list_paginator.page(page_number)
        except EmptyPage: 
            New_list_paginator_page = []

        New_list_paginator_page_data = serializer.NewsListSerializer(New_list_paginator_page, many = True)

        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": New_list_paginator_page_data.data
        }, status=200)
    except Exception as e:
        return Response({
            "status": False, 
            "message" : "Network request failed"
        }, status=500)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def news_details_view(request, id): 
    try:

        News_object = News_model.objects.get(id = id)

        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": {
                "news_image": News_object.image, 
                "new_title": News_object.name, 
                "news_description": News_object.description 
            }
        }, status=200)
    except Exception as e: 
        return Response({
            "status": False, 
            "message" : "Network request failed"
        }, status=500)