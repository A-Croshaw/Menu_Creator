from django import forms
from .models import Recipe, Ingredients, Method


class IngredientsForm(forms.ModelForm):
    """Ingredient Form"""
    
    class Meta:
        """
        Form Fields
        """
        model = Ingredients
        fields = (
                  'ingredient',
                  'quantity',
                  )
        labels = {
            'ingredient': 'Ingredient',
            'quantity': 'Quantity',
        }


class RecipeForm(forms.ModelForm):
    """Recipe Form"""

    class Meta:
        """
        Form Fields
        """
        model = Recipe
        fields = ("recipeName",
                  "description",
                  "recipecategory",
                  "recipesubcategory",
                  "portions",
                  )
        widget = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "recipeName": "Recipe Name",
            "description": "Description",
            "recipecategory": "Category",
            "recipesubcategory": "Sub Category",
            "portions": "Portions",
        }


class MethodForm(forms.ModelForm):
    """Method form"""

    class Meta:
        """
        Form Fields
        """

        model = Method
        fields = ("steps",
                  )
        widget = {
            "steps": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {
            "steps": "Steps",
        }