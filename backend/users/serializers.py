from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        SerializerMethodField, ValidationError)

from recipes.models import Recipe

from .models import Follow


User = get_user_model()


class CustomUserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()


class FollowSerializer(ModelSerializer):
    user = IntegerField(source='user.id')
    following = IntegerField(source='following.id')

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        user = data['user']['id']
        following = data['following']['id']
        follow_exist = Follow.objects.filter(
            user=user, following__id=following
        ).exists()
        if user == following:
            raise ValidationError(
                'Вы не можете подписаться на самого себя!'
            )
        if follow_exist:
            raise ValidationError('Вы уже подписаны на этого автора!')
        return data

    def create(self, validated_data):
        following = validated_data.get('following')
        following = get_object_or_404(User, pk=following.get('id'))
        user = validated_data.get('user')
        return Follow.objects.create(user=user, following=following)


class RecipesFollowingSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(CustomUserSerializer):
    recipes = SerializerMethodField()
    recipes_count = IntegerField(source='recipes.count')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        return RecipesFollowingSerializer(recipes, many=True).data
