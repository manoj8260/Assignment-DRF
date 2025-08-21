from django.shortcuts import render
from rest_framework import viewsets ,generics
from apps.recipes.serializers import RecipesSeriallizers ,RecipeRatingSerializer
from apps.recipes.models import Recipes ,RecipeRatings
from rest_framework.permissions import IsAuthenticated
from apps.recipes.permissions import IsSellerOrReadOnly ,IsCustomerOrReadOnly


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSeriallizers
    permission_classes =[IsAuthenticated,IsSellerOrReadOnly]
    
    
    def perform_create(self, serializer):  
        serializer.save()
        
class   RecipeRatingView(generics.ListCreateAPIView)  :
    queryset = RecipeRatings.objects.all()
    serializer_class = RecipeRatingSerializer
    permission_classes =[IsAuthenticated,IsCustomerOrReadOnly]
    
    def perform_create(self, serializer):  
        serializer.save()

class RecipeRatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeRatings.objects.all()
    serializer_class = RecipeRatingSerializer
    permission_classes = [IsAuthenticated,IsCustomerOrReadOnly]        