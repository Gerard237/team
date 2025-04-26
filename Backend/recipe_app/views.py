import json
from rest_framework import viewsets, status
from .models import Recipe, Comment, Favori
from .serializers import RecipeSerializer, CommentSerializer, FavoriSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

class RecipePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination

    @action(detail=False, methods=['get'])
    def filter_by_location(self, request):
        country = request.query_params.get('country', None)
        name = request.query_params.get('name', None)

        id_recipes = request.query_params.get('id_recipes', [])
        if id_recipes:
            try:
                id_recipes = json.loads(id_recipes)
                recipes = Recipe.objects.filter(id_recipe__in=id_recipes)
            except json.JSONDecodeError:
                return Response({"error": "Invalid format for id_recipes. Use a JSON array."}, status=status.HTTP_400_BAD_REQUEST)
        elif country and name:
            recipes = self.queryset.filter(country__iexact=country, name__iexact=name)
        elif country:
            recipes = self.queryset.filter(country__iexact=country)
        elif name:
            recipes = self.queryset.filter(name__iexact=name)
        else:
            recipes = self.queryset

        page = self.paginate_queryset(recipes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class FavoriViewSet(viewsets.ViewSet):

    def list(self, request):
        user = request.query_params.get('user', None)
        if user:
            favoris = Favori.objects.filter(user=user)
        else:
            favoris = Favori.objects.all()
        serializer = FavoriSerializer(favoris, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = FavoriSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request):
        user = request.data.get('user')
        id_recipe = request.data.get('id_recipe')
        if not user or not id_recipe:
            return Response({"error": "Both 'user' and 'id_recipe' are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            favori = Favori.objects.get(user=user, id_recipe=id_recipe)
            favori.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favori.DoesNotExist:
            return Response({"error": "Favori not found."}, status=status.HTTP_404_NOT_FOUND)