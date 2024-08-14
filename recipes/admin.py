from django.contrib import admin
from .models import Recipe, Ingredients, Method, RecipeCategory, RecipeSubcategory


class RecipeCategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Category
    """
    fieldsets = []
    list_display = (
        'view_recipecategory',
        'recipecategory',
    )
    ordering = ("recipecategory",)


class RecipeSubcategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Subcategory
    """
    fieldsets = []
    list_display = (
        'view_recipesubcategory',
        'recipesubcategory',
        'recipecategory'
    )
    list_filter = ("recipecategory",)
    ordering = ("recipecategory", "recipesubcategory",)


class IngredientsAdminInline(admin.TabularInline):
    """
    Creates Admin For The Ingredients
    """
    model = Ingredients
    readonly_fields = ('ingredientline_total',)


class MethodAdminInline(admin.StackedInline):
    """
    reates Admin For The Method
    """
    model = Method
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Main Part OF The Recipe And Adds Method
    And Ingredients To an Inline Output and Displays as one Item
    """
    fieldsets = []
    inlines = (IngredientsAdminInline, MethodAdminInline)
    list_filter = ("recipecategory", "recipesubcategory", "recipeName",)
    ordering = ("recipecategory", "recipesubcategory", "recipeName",)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients)
admin.site.register(Method)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
admin.site.register(RecipeSubcategory, RecipeSubcategoryAdmin)
