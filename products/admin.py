from django.contrib import admin
from .models import Product, Category, Subcategory


class ProductAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Products
    """
    fieldsets = []

    list_display = (
        "name",
        "category",
        "subcategory",
        "cost",
        "weight",
        "quantity",
        "liquid_vol"
    )

    list_filter = ("category", "subcategory", "name",)
    ordering = ("category", "subcategory", "name",)


class CategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Category
    """
    fieldsets = []
    list_display = (
        'view_category',
        'category',
    )
    ordering = ("category",)


class SubcategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Subcategory
    """
    fieldsets = []
    list_display = (
        'view_subcategory',
        'subcategory',
        'category'
    )
    list_filter = ("category",)
    ordering = ("category", "subcategory",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
