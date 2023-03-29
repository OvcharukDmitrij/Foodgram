from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        'название',
        max_length=200,
        help_text ='введите название ингредиента',
    )

    measurement_unit = models.CharField(
        'единицы измерения',
        max_length=200,
        help_text='укажите единицы измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __repr__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        'тэг',
        max_length=200,
        help_text ='введите тэг',
        unique=True,
    )
    color = models.CharField(
        'цвет',
        max_length=7,
        help_text='укажите HEX-код цвета',
        unique=True
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        help_text='укажите slug',
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __repr__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(
        'название',
        max_length=200,
        help_text='введите название рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='автор рецепта',
        help_text='укажите имя пользователя'
    )
    image = models.ImageField(
        'изображение',
        upload_to='recipes/images/',
        help_text='добавьте изображение рецепта'
    )
    text = models.TextField(
        'описание',
        help_text='напишите описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='тег'
    )
    cooking_time = models.IntegerField(
        'время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
        help_text='укажите время приготовления блюда'
    )

    def __repr__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    """Модель многие-ко-многим Рецепты-Ингредиенты и количество."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredient',
        verbose_name='рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredient',
        verbose_name='ингредиент'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество'
    )

    def __repr__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    """Модель многие-ко-многим Рецепты-Теги."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __repr__(self):
        return f'{self.recipe} {self.tag}'


class RecipeFavorite(models.Model):
    """Модель многие-ко-многим ИзбранныйРецепт-Пользователь."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='пользователь'
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='рецепт для добавление в избранное'
    )

    def __repr__(self):
        return f'{self.user} {self.favorite_recipe}'


class ShoppingCart(models.Model):
    """Список покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='пользователь'
    )
    recipe_buy = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='рецепт для покупки ингредиентов'
    )

