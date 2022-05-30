from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()

router.register('recipes', RecipeViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
