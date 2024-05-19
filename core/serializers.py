from rest_framework import serializers
from core.models import Ingredient, Category, Recipe, RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), write_only=True)  # For POST/PUT
    quantity = serializers.CharField()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'ingredient_id', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Show author's username
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)  # Nested serialization
    categories = CategorySerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'author', 'description', 'ingredients', 'categories', 'image']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        categories_data = validated_data.pop('categories')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        recipe.categories.set(categories_data)
        return recipe