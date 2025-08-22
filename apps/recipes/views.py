from django.shortcuts import render
from rest_framework import viewsets, generics
from apps.recipes.serializers import RecipesSeriallizers, RecipeRatingSerializer
from apps.recipes.models import Recipes, RecipeRatings
from rest_framework.permissions import IsAuthenticated
from apps.recipes.permissions import IsSellerOrReadOnly, IsCustomerOrReadOnly
from apps.recipes.tasks import resize_recipe_image  ,backup_user_data
from django.http import JsonResponse
from apps.recipes.tasks import send_daily_emails
from rest_framework.views import APIView
from rest_framework.response import Response
import os


class RecipesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for creating, updating, deleting, and listing recipes.
    Only sellers can create or modify recipes.
    """
    queryset = Recipes.objects.all()
    serializer_class = RecipesSeriallizers
    permission_classes = [IsAuthenticated, IsSellerOrReadOnly]

    def perform_create(self, serializer):
        recipe = serializer.save()
        if recipe.recipe_image and recipe.recipe_image.name:
            full_path = recipe.recipe_image.path  # absolute path
            if full_path and os.path.exists(full_path):
                # Trigger async task
                resize_recipe_image.delay(recipe.id, recipe.recipe_image.name)


class RecipeRatingView(generics.ListCreateAPIView):
    """
    List all ratings for recipes and allow customers to create a rating.
    """
    queryset = RecipeRatings.objects.all()
    serializer_class = RecipeRatingSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save()


class RecipeRatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific recipe rating.
    Only the customer who created the rating can modify it.
    """
    queryset = RecipeRatings.objects.all()
    serializer_class = RecipeRatingSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]
    


def trigger_daily_emails(request):
    """
    Trigger the Celery task to send daily emails.
    """
    try:
        # Trigger asynchronously
        send_daily_emails.delay()
        return JsonResponse({"status": "success", "message": "Daily email task triggered."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

class TriggerBackupView(APIView):
    def post(self, request):
        backup_user_data.delay()
        return Response({"message": "Backup task triggered successfully"})
    