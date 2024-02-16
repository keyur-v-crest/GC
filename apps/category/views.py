from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes 
from apps.category.serializer import CreateCategorySerializer, UpdateCategorySerializer, FetchCategoryList
from apps.category.models import Details as Category_details 

@api_view(["POST"])
def CreateCategory(request): 
    try:

        if CreateCategorySerializer(data = request.data).is_valid(): 
            
            Create_category = Category_details.objects.create(
                category_name = request.data['name'], 
                category_image = request.data['image']
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
def UpdateCategory(request): 
    try: 
        
        if UpdateCategorySerializer(data = request.data).is_valid():
            
            Category_objetct = Category_details.objects.get(id = request.data['id']) 
            Category_objetct.category_name = request.data['name'] 
            Category_objetct.category_image = request.data['image']
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
def FetchCategory(request): 
    try:

        Category_data = Category_details.objects.all()
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