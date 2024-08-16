from django.db import models
import os
import uuid
from django.contrib.auth.models import User

def get_unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('uploads/', unique_filename)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "category"

    
class Difficulty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "difficulty"

class Recipes(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    level = models.ForeignKey(Difficulty, models.DO_NOTHING, blank=True, null=True, db_index=True)
    recipe_name = models.TextField(blank=True, null=True, db_index=True)
    # image_filename = models.TextField(blank=True, null=True)
    image_filename = models.FileField(upload_to=get_unique_filename, blank=True, null=True)
    time_cook = models.IntegerField(blank=True, null=True)
    # categoryId = models.IntegerField(blank=True, null=True)
    # levelId = models.IntegerField(blank=True, null=True)
    ingridient = models.TextField(blank=True, null=True)
    how_to_cook = models.TextField(blank=True, null=True)
    is_favorite = models.BooleanField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=False, default=False)
    created_by = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField(blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "recipes"
        
class FavoriteFood(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    recipe = models.ForeignKey(Recipes, models.DO_NOTHING, blank=True, null=True)
    is_favorite = models.BooleanField(blank=True, null=True, default=True)

    class Meta:
        db_table = "favorite_food"

