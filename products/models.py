from django.db import models

class Category(models.Model):
    """ Creates Categories OF Products """
    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'categories'

    category = models.CharField(max_length=254)
    view_category = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.category)

    def get_view_category(self):
        return self.view_category


class Subcategory(models.Model):
    """ Creates Sub Categories of the Products """

    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'subcategories'

    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL)
    subcategory = models.CharField(max_length=254)
    view_subcategory = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.subcategory)

    def get_view_subcategory(self):
        return self.view_subcategory


class Product(models.Model):
    """
    A model to create and manage Products
    """

    subcategory  = models.ForeignKey(
        'Subcategory', null=True, blank=True,
        on_delete=models.SET_NULL)
    category  = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL)
    cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
    )
    product_name = models.CharField(max_length=254, null=False
                                    )
    weight = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        default=0
    )
    liquid_vol = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        default=0
    )
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        default=0
    )


    class Meta:
        ordering = ["product_name"]

    def __str__(self):
        return str(self.product_name)
