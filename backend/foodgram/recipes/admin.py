from django.contrib import admin

from .models import (Recipe, Tag, Ingredient, RecipeIngredient,
                     RecipeFavorite, RecipeTag, ShoppingCart)


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = ('name', 'author', 'favorite',)
    search_fields = ('author', 'name',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'
    inlines = [TagInline, IngredientInline]

    def favorite(self, obj):
        return RecipeFavorite.objects.filter(favorite_recipe=obj).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)


@admin.register(RecipeFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):

    list_display = ('user', 'favorite_recipe',)
    search_fields = ('user',)


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):

    list_display = ('id', 'recipe', 'tag',)
    search_fields = ('tag',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe_buy',)
    search_fields = ('user',)

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    search_fields = ('recipe',)
