from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user,
                                     following=obj).exists()


class RecipesFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    following = serializers.IntegerField(source='author.id')

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        user = data['user']['id']
        following = data['following']['id']
        if user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        if Follow.objects.filter(user=user,
                                 following__id=following).exists():
            raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя')
        return data

    def create(self, validated_data):
        following = validated_data.get('following')
        following = get_object_or_404(User, pk=following.get('id'))
        user = validated_data.get('user')
        return Follow.objects.create(user=user, following=following)


class FollowListSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes.count')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = fields

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        return RecipesFollowingSerializer(recipes, many=True).data
