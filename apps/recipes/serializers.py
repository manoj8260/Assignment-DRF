from rest_framework import serializers
from apps.recipes.models import  Recipes ,RecipeRatings

class RecipesSeriallizers(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving recipes.
    Only sellers are allowed to create recipes.
    """
    class Meta :
        model = Recipes
        fields =('id','name','description','recipe_image','created_at','updated_at','created_by')
        read_only_fields = ('id','created_at','updated_at','created_by')
        
    def validate_name(self, value):
        if len(value) <3 :
            raise serializers.ValidationError('Recipe name must be at least 3 characters long.')
        return value
    
    def validate_description(self, value):
      if len(value) < 10 or len(value) > 100:
        raise serializers.ValidationError(
            "description must be between 10 and 100 characters long."
        )
      return value
  
    def create(self, validated_data):
        user =self.context['request'].user
        print(user)
        if user.user_type != 'seller':
            raise serializers.ValidationError('Only sellers can create recipes.')
       
        validated_data['created_by'] = user
        return super().create(validated_data)

   
   
class  RecipeRatingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving recipe ratings.
    Each user can rate a recipe only once.
    """
    class Meta :
        model = RecipeRatings
        fields = ('id','recipe','user','rating')  
        read_only_fields = ('id','user')  
            
    def validate(self, attrs):
        user = self.context['request'].user
        recipe =  attrs.get('recipe')
        
        if RecipeRatings.objects.filter(recipe=recipe,user=user).exists():
            raise serializers.ValidationError(
                 {
                     "message": "You have already rated this recipe."
                },      
            )  
        return attrs
    def create(self, validated_data):
        print(self.context['request'].user)
        validated_data['user'] =self.context['request'].user
       
        return super().create(validated_data)     