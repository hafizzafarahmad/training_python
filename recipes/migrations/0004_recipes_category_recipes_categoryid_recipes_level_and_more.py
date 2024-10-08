# Generated by Django 5.1 on 2024-08-15 07:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_category_table_alter_difficulty_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recipes.category'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='categoryId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipes',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='recipes.difficulty'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='levelId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recipes',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
