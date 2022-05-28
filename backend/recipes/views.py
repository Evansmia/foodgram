from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from foodgram.pagination import CustomPaginator

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientsInRecipe,
                     Recipe, ShoppingList, Tag)
from .permissions import IsOwnerOrReadOnly
from .serializers import (AddRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingListSerializer, TagSerializer)


class ListAndRetriveViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass


class IngredientsViewSet(ListAndRetriveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = IngredientFilter
    pagination_class = None


class TagsViewSet(ListAndRetriveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return AddRecipeSerializer

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_list = get_object_or_404(ShoppingList,
                                          user=user, recipe=recipe)
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user_shopping_list = request.user.shopping_list.all()
        to_buy = get_ingredients_list(user_shopping_list)
        return download_file_response(to_buy, 'to_buy.txt')


def get_ingredients_list(recipes_list):
    ingredients_dict = {}
    for recipe in recipes_list:
        ingredients = IngredientsInRecipe.objects.filter(recipe=recipe.recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in ingredients_dict:
                ingredients_dict[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                    }
            else:
                ingredients_dict[name]['amount'] += amount
    to_buy = []
    for item in ingredients_dict:
        to_buy.append(f'{item} - {ingredients_dict[item]["amount"]} '
                      f'{ingredients_dict[item]["measurement_unit"]} \n')
    return to_buy


def download_file_response(list_to_download, filename):
    response = HttpResponse(list_to_download, 'Content-Type: text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
