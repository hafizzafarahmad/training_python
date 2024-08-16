from rest_framework import serializers
from .models import Recipes, Category, Difficulty, FavoriteFood
from django.contrib.auth.models import User
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = '__all__'
        
class RecipesSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(source='category', read_only=True)
    difficulties = DifficultySerializer(source='level', read_only=True)
    
    class Meta:
        model = Recipes
        fields = '__all__'
        
class FavRecipesSerializer(serializers.ModelSerializer):
    recipes = RecipesSerializer(source='recipe', read_only=True)
    
    class Meta:
        model = FavoriteFood
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user