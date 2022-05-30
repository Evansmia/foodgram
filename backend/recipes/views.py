from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from foodgram.pagination import CustomPaginator

from .filters import RecipeFilter
from .models import (Favorite, Ingredient, IngredientsInRecipe,
                     Recipe, ShoppingList, Tag)
from .permissions import IsAdminOrOwner
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
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend]
    search_fields = ('^name',)
    pagination_class = None


class TagsViewSet(ListAndRetriveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrOwner)
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return AddRecipeSerializer

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        data = {'user': request.user.id, 'recipe': recipe.id}
        serializer = FavoriteSerializer(data=data)
        if request.method == 'POST':
            if Favorite.objects.filter(
                    recipe=recipe, user=request.user).exists():
                raise ValidationError(
                    'Данный рецепт уже есть в Вашем списке избранных!'
                )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = get_object_or_404(
                Favorite, user=request.user, recipe__id=id
            )
            favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST', 'DELETE'],
            url_path=r'(?P<id>\d+)/shopping_cart/',
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        data = {'user': request.user.id, 'recipe': recipe.id}
        serializer = ShoppingListSerializer(data=data)
        if request.method == 'POST':
            if ShoppingList.objects.filter(
                    recipe=recipe, user=request.user).exists():
                raise ValidationError(
                    'Вы уже добавили данный рецепт в список покупок!'
                )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            shopping_list = get_object_or_404(
                ShoppingList, user=request.user, recipe__id=id
            )
            shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
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
