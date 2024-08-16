from django import forms
from .models import Recipe, Ingredients, Method, RecipeCategory, RecipeSubcategory


class IngredientsForm(forms.ModelForm):
    """Ingredient Form"""

    class Meta:
        """
        Form Fields
        """
        model = Ingredients
        fields = {'ingredient',
                  'quantity',
                  'unit'
                  }
        labels = {
            'ingredient': 'Ingredient',
            'quantity': 'Quantity',
            'unit': 'Unit',
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
        labels = {
            "recipeName": "Recipe Name",
            "description": "Description",
            "recipecategory": "Category",
            "recipesubcategory": "SubCategory",
            "portions": "Portions",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subcategory = RecipeSubcategory.objects.all()
        view_recipesubcategory = [
            (s.id, s.get_view_recipesubcategory()) for s in subcategory]
        self.fields['recipesubcategory'].choices = view_recipesubcategory
        category = RecipeCategory.objects.all()
        view_recipecategory = [(c.id, c.get_view_recipecategory())
                               for c in category]
        self.fields['recipecategory'].choices = view_recipecategory
        self.fields['recipeName'].widget.attrs['autofocus'] = True
        self.fields['description'].widget.attrs = {'rows': 3}


class MethodForm(forms.ModelForm):
    """Method form"""

    class Meta:
        """
        Form Fields
        """

        model = Method
        fields = ("steps",
                  )
        labels = {
            "steps": "Steps",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['steps'].widget.attrs = {'rows': 2}
