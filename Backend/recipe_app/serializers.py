from rest_framework import serializers
from .models import Recipe, Comment, Favori

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class FavoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favori
        fields = '__all__'
