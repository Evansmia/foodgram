from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientsInRecipe,
                     Recipe, ShoppingList, Tag)


class IngredientsInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe__name', 'ingredient__name')


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    list_filter = ['name']
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'in_favorite'
    )
    list_filter = ['name', 'author', 'tags']
    inlines = (IngredientsInRecipeInline,)

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(
    IngredientsInRecipe,
    IngredientsInRecipeAdmin
)
