import logging
import bcrypt
from rest_framework import generics, pagination, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from .models import Recipes, Category, Difficulty, FavoriteFood
from .serializers import RecipesSerializer, UserSerializer, CategorySerializer, DifficultySerializer, FavRecipesSerializer
from .permission import IsOwnerOrReadOnly
from django.urls import path
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

# HELPER
class RecipesPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
        
# GET CATEGORY
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = RecipesPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                'message': 'Category retrieved successfully.',
                'status': status.HTTP_200_OK,
                'next': paginated_response.data['next'],
                'previous': paginated_response.data['previous'],
                'total': paginated_response.data['count'],
                'data': paginated_response.data['results']
            }, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Category retrieved successfully.',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

# GET DIFFICULTY
class DifficultyListCreateView(generics.ListCreateAPIView):
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer
    pagination_class = RecipesPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                'message': 'Category retrieved successfully.',
                'status': status.HTTP_200_OK,
                'next': paginated_response.data['next'],
                'previous': paginated_response.data['previous'],
                'total': paginated_response.data['count'],
                'data': paginated_response.data['results']
            }, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Category retrieved successfully.',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

# GET/POST RECIPES
class RecipesListCreateView(generics.ListCreateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = RecipesPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        userId = request.query_params.get('userId')
        search_query = request.query_params.get('recipeName')
        category_query = request.query_params.get('categoryId')
        difficulty_query = request.query_params.get('levelId')
        sort_by = self.request.query_params.get('sort', 'asc')
        
        if userId:
            queryset = queryset.filter(user_id__exact=userId)
        
        if search_query:
            queryset = queryset.filter(recipe_name__icontains=search_query)
            
        if category_query:
            queryset = queryset.filter(category__id__icontains=category_query)
            
        if difficulty_query:
            queryset = queryset.filter(level__id__icontains=difficulty_query)
            
        if sort_by == 'desc':
            queryset = queryset.order_by('-recipe_name')
        else:
            queryset = queryset.order_by('recipe_name') 
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                'message': 'Recipes retrieved successfully.',
                'status': status.HTTP_200_OK,
                'next': paginated_response.data['next'],
                'previous': paginated_response.data['previous'],
                'total': paginated_response.data['count'],
                'data': paginated_response.data['results']
            }, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Recipes retrieved successfully.',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    def create(self, request):
        file = request.FILES.get('image_filename')
        if file:
            data = request.data.copy()
            data['image_filename'] = file 

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({
                    'message': 'Recipe created successfully.',
                    'status': status.HTTP_200_OK,
                    'data': serializer.data
                }, status=status.HTTP_200_OK, headers=headers)
            
            return Response({
                'message': 'Invalid data.',
                'status': status.HTTP_400_BAD_REQUEST,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'No file uploaded.',
            'status': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
 
 # GET/POST RECIPES

# GET DETAIL RECIPES
class RecipesDetailCreateView(generics.ListCreateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recipe_id = request.query_params.get('recipe_id')

        if not recipe_id:
            return Response({
                "message": "recipe_id is required.",
                "statusCode": status.HTTP_400_BAD_REQUEST,
                "status": "Error",
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = Recipes.objects.filter(recipe_id=recipe_id).first()

        if not queryset:
            return Response({
                "message": "Recipe not found.",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "status": "Error",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset)
        response_data = {
            "data": serializer.data,
            "message": "Recipe retrieved successfully.",
            "statusCode": status.HTTP_200_OK,
            "status": "Success",
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

# GET/POST MY FAVORITE RECIPES
class MyFavListCreateView(generics.ListCreateAPIView):
    queryset = FavoriteFood.objects.all()
    serializer_class = FavRecipesSerializer
    pagination_class = RecipesPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(is_favorite__exact=True)
        
        userId = request.query_params.get('userId')
        sort_by = self.request.query_params.get('sort', 'asc')
        
        if userId:
            queryset = queryset.filter(user_id__exact=userId)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                'message': 'Recipes retrieved successfully.',
                'status': status.HTTP_200_OK,
                'next': paginated_response.data['next'],
                'previous': paginated_response.data['previous'],
                'total': paginated_response.data['count'],
                'data': paginated_response.data['results']
            }, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'message': 'Recipes retrieved successfully.',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
# DELETE RECIPES
class RecipesDeleteView(generics.DestroyAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    
# PUT RECIPES
class RecipesRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        file = request.FILES.get('image_filename')
        if file:
            data = request.data.copy()
            data['image_filename'] = file
        else:
            data = request.data

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Recipe updated successfully.',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

# PUT RECIPES FAVORITE
# class RecipesUpdateFavoriteView(generics.RetrieveUpdateAPIView):
#     queryset = Recipes.objects.all()
#     serializer_class = RecipesSerializer
    
#     def update(self, request, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()

#         if 'is_favorite' in request.data:
#             data = {'is_favorite': request.data['is_favorite']}
#         else:
#             return Response({
#                 'message': 'is_favorite field is required.',
#                 'status': status.HTTP_400_BAD_REQUEST,
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Perform the update
#         serializer = self.get_serializer(instance, data=data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         return Response({
#             'message': 'Recipe updated successfully.',
#             'status': status.HTTP_200_OK,
#             'data': serializer.data
#         }, status=status.HTTP_200_OK)

class RecipesUpdateFavoriteView(generics.RetrieveUpdateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'is_favorite' in request.data:
            is_favorite = request.data['is_favorite']
            data = {'is_favorite': is_favorite}
        else:
            return Response({
                'message': 'is_favorite field is required.',
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        user_id = request.user
        recipe = instance
        
        favorite_record, created = FavoriteFood.objects.update_or_create(
            user=user_id,
            recipe=recipe,
            is_favorite=is_favorite
        )

        if not created:
            favorite_record.is_favorite = is_favorite
            favorite_record.save()
            
        if request.data['is_favorite'] == False:
            FavoriteFood.objects.filter(user=user_id, recipe=recipe).delete()
            return Response({
                'message': 'Recipe updated and favorite status removed successfully.',
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Recipe updated successfully.',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

# POST REGISTER
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "statusCode": status.HTTP_200_OK,
                    "status": "Success",
                    "message": request.data.get("username"),
                }

                # logger.info(f"User registered successfully: {request.data.get('username')}")
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "status": "Failed",
                    "message": "Register Error",
                    "errors": serializer.errors,
                }

                # logger.warning(f"Failed user registration: {serializer.errors}")
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# POST LOGIN
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            password_str = str(password)

            user = User.objects.filter(username=username).first()

            if user and user.check_password(password_str):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    "data": {
                        "id": user.id,
                        "token": access_token,
                        "username": user.username,
                        "email": user.email,
                    },
                    "message": "Login Success",
                    "statusCode": status.HTTP_200_OK,
                    "status": "Success",
                }

                # logger.info(f"Successful login for user: {user.username}")
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "message": "ErrorMessages.ERR_SIGN_IN",
                    "statusCode": status.HTTP_401_UNAUTHORIZED,
                    "status": "Failed",
                }

                # logger.warning(f"Failed login attempt for username: {username}")
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            response_data = {
                "message": "Error Code",
                "statusCode": status.HTTP_401_UNAUTHORIZED,
                "status": "Failed",
            }
            # logger.error(f"An error occurred during login: {str(e)}")
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

# API PROTECTED TOKEN
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view"})

# class GetUser():
#     user = User.objects.get(username='Hafiz')
#     token, created = Token.objects.get_or_create(user=user)
#     print(token.key)