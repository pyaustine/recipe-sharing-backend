from django.contrib import admin
from .models import Ingredient, Category, Recipe, RecipeIngredient

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)