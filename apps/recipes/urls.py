from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from apps.recipes.views import RecipesViewSet ,RecipeRatingView ,RecipeRatingDetailView


recipes_router = DefaultRouter()


recipes_router.register(r'recipes',RecipesViewSet,basename='recipes')


urlpatterns =[
    path('v1/',include(recipes_router.urls)),
    path("ratings/", RecipeRatingView.as_view(), name="recipe-rating-list-create"),
    path("ratings/<int:pk>/", RecipeRatingDetailView.as_view(), name="recipe-rating-detail"),
    
]





