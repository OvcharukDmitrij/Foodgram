from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        help_text ='введите название ингредиента',
    )
    quantity = models.IntegerField(
        'количество',
        validators=[MinValueValidator(1)],
        help_text='укажите количество'
    )

    measurement_unit = models.CharField(
        'единицы измерения',
        max_length=200,
        help_text='укажите единицы измерения'
    )

    def __repr__(self):
        return self.name


class Tag(models.Model):
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

    def __repr__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        help_text='введите название рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        help_text='укажите имя пользователя'
    )
    image = models.ImageField(
        'изображение',
        upload_to='recipes',  # Тут нужно понять...
        help_text='добавьте изображение рецепта'
    )
    description = models.TextField(
        'описание',
        help_text='напишите описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
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
        verbose_name = "Рецепты"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __repr__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __repr__(self):
        return f'{self.recipe} {self.tag}'