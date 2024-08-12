from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """ Product instance Form"""

    class Meta:
        """
        Form Fields
        """
        model = Product
        fields = ("product_name",
                  "category",
                  "subcategory",
                  "cost",
                  "weight",
                  "quantity",
                  "liquid_vol" 
                  )
        labels = {"product_name": "Product Name",
                  "category": "Category",
                  "subcategory": "Subcategory",
                  "cost": "Cost",
                  "weight": "Weight",
                  "quantity": "Quantity",
                  "liquid_vol" : "Volume" 
                  }