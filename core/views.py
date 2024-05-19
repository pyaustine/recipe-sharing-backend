from rest_framework import viewsets, permissions
from core.models import Recipe, RecipeIngredient, Ingredient, Category
# from core.serializers import RecipeSerializer

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Recipe, Ingredient, Category
from core.serializers import RecipeSerializer, RecipeIngredientSerializer, IngredientSerializer, CategorySerializer



# recipes/views.py

from django.http import JsonResponse
from django.contrib.auth.models import User

def dummy_view(request):
    # Dummy user data
    dummy_users = [
        {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'password123',
        },
        {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'password456',
        },
        # Add more dummy users as needed
    ]

    # Dummy ingredient data
    dummy_ingredients = [
        {
            'name': 'Flour',
        },
        {
            'name': 'Sugar',
        },
        {
            'name': 'Eggs',
        },
        # Add more dummy ingredients as needed
    ]

    # Dummy category data
    dummy_categories = [
        {
            'name': 'Dessert',
        },
        {
            'name': 'Main Dish',
        },
        # Add more dummy categories as needed
    ]

    # Dummy recipe data
    dummy_recipes = [
        {
            'title': 'Chocolate Cake',
            'author': 'user1',
            'description': 'Decadent chocolate cake with rich frosting.',
            'ingredients': ['Flour', 'Sugar', 'Eggs'],
            'categories': ['Dessert'],
            'image': 'path/to/chocolate_cake_image.jpg',
        },
        {
            'title': 'Spaghetti Carbonara',
            'author': 'user2',
            'description': 'Classic Italian pasta dish with eggs, cheese, pancetta, and pepper.',
            'ingredients': ['Spaghetti', 'Eggs', 'Pancetta'],
            'categories': ['Main Dish'],
            'image': 'path/to/spaghetti_carbonara_image.jpg',
        },
        # Add more dummy recipes as needed
    ]

    return JsonResponse({
        'users': dummy_users,
        'ingredients': dummy_ingredients,
        'categories': dummy_categories,
        'recipes': dummy_recipes,
    })

class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Recipe model, providing CRUD operations and additional actions.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # Optional: Set permissions (e.g., IsAuthenticatedOrReadOnly) if needed.

    @action(detail=True, methods=['get'])
    def ingredients(self, request, pk=None):
        """
        List all ingredients for a specific recipe.
        """
        recipe = self.get_object()
        ingredients = recipe.ingredients.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new recipe, including its ingredients and categories.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update an existing recipe (ingredients and categories are replaced).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

from rest_framework import viewsets

from core.models import Category
from core.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model, providing CRUD operations.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Optional: Set permissions (e.g., IsAuthenticatedOrReadOnly) if needed.