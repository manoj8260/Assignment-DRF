from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.recipes.views import RecipesViewSet, RecipeRatingView, RecipeRatingDetailView


# Router for Recipe 
recipes_router = DefaultRouter()
# Registers recipe_router
recipes_router.register(r'recipes', RecipesViewSet, basename='recipes')


urlpatterns = [
    # Include all router-generated recipe endpoints 
    path('v1/', include(recipes_router.urls)),

    # List all ratings or create a new rating
    path("ratings/", RecipeRatingView.as_view(), name="recipe-rating-list-create"),

    # Retrieve, update, or delete a specific rating
    path("ratings/<int:pk>/", RecipeRatingDetailView.as_view(), name="recipe-rating-detail"),
]
