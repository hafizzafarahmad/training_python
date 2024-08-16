"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('master/category/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('master/difficulty/', DifficultyListCreateView.as_view(), name='difficulty-list-create'),
    path('recipes/', RecipesListCreateView.as_view(), name='recipes-list-create'),
    path('recipes/<int:pk>/', RecipesDeleteView.as_view(), name='recipes-delete'),
    path('recipes/detail', RecipesDetailCreateView.as_view(), name='recipes-detail'),
    path('recipes/update/<int:pk>/', RecipesRetrieveUpdateView.as_view(), name='recipes-retrieve-update'),
    path('recipes/favorite/<int:pk>/', RecipesUpdateFavoriteView.as_view(), name='recipes-favorite-create'),
    path('recipes/favorite/', MyFavListCreateView.as_view(), name='recipes-favorite-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("sign-up/", RegisterView.as_view(), name="register"),
    path("signin/", LoginView.as_view(), name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
