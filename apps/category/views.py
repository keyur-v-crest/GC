from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication 
from apps.category.serializer import CreateCategorySerializer, UpdateCategorySerializer, FetchCategoryList
from apps.category.models import Details as Category_details 
from apps.user.helpers import CheckUserAuthentication

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def category_create_view(request): 
    try:

        if CreateCategorySerializer(data = request.data).is_valid(): 
            
            Create_category = Category_details.objects.create(
                category_name = request.data['name'], 
                category_image = request.data['image'], 
                # type = request.data['type'],  
                is_active = request.data['is_active']
            )
            Create_category.save() 

            return Response({
                'status': True, 
                'message': "Create"
            }, status=200)
        
        else:
            return Response({
                'status': False, 
                'message': "Failed to create category"
            }, status=400)
    
    except Exception as e: 
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def category_update_view(request, id): 
    try: 
        
        if CreateCategorySerializer(data = request.data).is_valid():
            
            Category_objetct = Category_details.objects.get(id = id) 
            Category_objetct.category_name = request.data['name'] 
            Category_objetct.category_image = request.data['image']
            # Category_objetct.type = request.data['type']
            Category_objetct.is_active = request.data['is_active']
            Category_objetct.save()

            return Response({
                'status': True, 
                'message': "Update category successfully"
            }, status = 200)
        else:
            return Response({
                'status': False,
                'message': "Failed to update category"
            }, status = 400)
    except Exception as e:

        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)  
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def category_list_view(request): 
    try:
        Category_data = Category_details.objects.all().order_by("-id")
        Category_data = FetchCategoryList(Category_data, many = True)
        return Response({
            'status': True, 
            'message': "Fetch", 
            'data': Category_data.data
        }, status=200)
    
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)  
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def category_selection_view(request):
    try:
        Category_data = Category_details.objects.filter(is_active = True).order_by("-id")
        Category_data = FetchCategoryList(Category_data, many = True)
        return Response({
            "status" : True, 
            "messgae": "Fetch", 
            "data": Category_data.data
        }, status=200) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)  

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([CheckUserAuthentication])
def category_details_view(request, id):
    try:

        Category_data = Category_details.objects.get(id = id)
        return Response({
            "status": True, 
            "message": "Fetch", 
            "data": {
                "category_name": Category_data.category_name, 
                "category_image": Category_data.category_image, 
                "is_active": Category_data.is_active
            }
        }, status=200) 
    except Exception as e:
        return Response({
            'status': False, 
            'message': "Network request failed"
        }, status=500)  
