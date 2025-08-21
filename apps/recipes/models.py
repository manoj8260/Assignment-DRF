from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipes(models.Model):
    name = models.CharField(
        max_length=255, 
        help_text=_("Name of the recipe")
        )
    description = models.TextField(
        help_text=_( "Description of the recipe")
    )
    recipe_image = models.ImageField(
        upload_to='recipes/',blank=True,null=True,
        help_text= _("Image of the recipe")
        )
    created_at= models.DateTimeField(
        auto_now_add=True,
        help_text= _("Recipe Created")
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("Recipe updated")
        )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        limit_choices_to={'user_type': 'seller'},
        help_text=_("User who created this recipe")
    )
    def __str__(self):
        return f"{self.name} by {self.created_by.first_name}"
    class Meta :
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        

class RecipeRatings(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ratings',
        help_text=_("Recipe being rated")
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings',
        help_text=_("User giving the rating")
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text=_("Rating from 1 to 5 stars")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return f"{self.user.email} rated {self.recipe.name} → {self.rating}*"

    class Meta :
        db_table = 'recipe_rating'
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
        unique_together = ['recipe', 'user']  
            