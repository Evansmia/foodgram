from enum import Enum
from django_filters import rest_framework as filters
from django_filters.filters import (AllValuesMultipleFilter,
                                    NumberFilter)

from .models import Recipe


class IsFavorited(Enum):
    IN = 1
    NOT_IN = 0


class IsInCart(Enum):
    IN = 1
    NOT_IN = 0


class RecipeFilter(filters.FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = NumberFilter(method='get_favorite')
    is_in_shopping_cart = NumberFilter(method='get_shopping')

    def get_favorite(self, queryset, name, value):
        user = self.request.user
        if value == IsFavorited.IN.value and user.is_authenticated:
            return queryset.filter(in_favorite__user=user)
        return queryset

    def get_shopping(self, queryset, name, value):
        user = self.request.user
        if value == IsInCart.IN.value and user.is_authenticated:
            return queryset.filter(shoppinglist__user=user)
        return

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'tags', 'is_in_shopping_cart')
