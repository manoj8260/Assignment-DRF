from django.contrib import admin
from apps.recipes.models import Recipes ,RecipeRatings

admin.site.register(Recipes)
admin.site.register(RecipeRatings)