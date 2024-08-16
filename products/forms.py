from django import forms
from .models import Product, Category, Subcategory


class ProductForm(forms.ModelForm):
    """ Product instance Form"""

    class Meta:
        """
        Form Fields
        """
        model = Product
        fields = ("name",
                  "category",
                  "subcategory",
                  "cost",
                  "weight",
                  "quantity",
                  "liquid_vol" 
                  )
        labels = {"name": "Product Name",
                  "category": "Category",
                  "subcategory": "Subcategory",
                  "cost": "Cost",
                  "weight": "Weight 'g' ",
                  "quantity": "Quantity",
                  "liquid_vol" : "Volume 'ml'" 
                  }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subcategory = Subcategory.objects.all()
        view_subcategory = [
            (s.id, s.get_view_subcategory()) for s in subcategory]
        self.fields['subcategory'].choices = view_subcategory
        category = Category.objects.all()
        view_category = [(c.id, c.get_view_category())
                               for c in category]
        self.fields['category'].choices = view_category
