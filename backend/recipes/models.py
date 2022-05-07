from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Название',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Введите название тега'
    )
    color = ColorField(
        max_length=7,
        unique=True,
        verbose_name='Цвет',
        help_text='Выберите цвет тега'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг',
        help_text='Введите слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name='Название',
        help_text='Введите название рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Введите автора'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        null=False,
        verbose_name='Изображение блюда',
        help_text='Загрузите изображение блюда'
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание',
        help_text='Введите описание рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        related_name='recipes',
        verbose_name='Теги',
        help_text='Выберите теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Время приготовления',
        help_text='Введите время приготовления',
        validators=(
            MinValueValidator(
                settings.MIN_COOK_TIME,
                f'Минимальное время: {settings.MIN_COOK_TIME} минута'
            ),
        )
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_user_favorite'
            ),
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_shopping_cart'
            ),
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
