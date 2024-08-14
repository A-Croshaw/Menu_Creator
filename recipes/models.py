from decimal import Decimal
from django.db import models
from django.db.models import Sum
from products.models import Product


class RecipeCategory(models.Model):
    """ Creates Categories for the Recipes """
    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'recipecategories'

    recipecategory = models.CharField(max_length=254)
    view_recipecategory = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.recipecategory)

    def get_view_category(self):
        return self.view_recipecategory


class RecipeSubcategory(models.Model):
    """ Creates Sub Categories for the Recipes """

    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'recipesubcategories'

    recipecategory = models.ForeignKey(
        'RecipeCategory', null=True, blank=True,
        on_delete=models.SET_NULL)
    recipesubcategory = models.CharField(max_length=254)
    view_recipesubcategory = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.recipesubcategory)

    def get_view_recipesubcategory(self):
        return self.view_recipesubcategory


class Recipe(models.Model):
    """A Model To Create A Recipes"""

    recipeName = models.CharField(
        max_length=300,
        null=True,
        blank=False
    )
    description = models.TextField()
    recipecategory = models.ForeignKey(
        'RecipeCategory', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    recipesubcategory = models.ForeignKey(
        'RecipeSubcategory', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    cost = models.DecimalField(
        max_digits=6, decimal_places=2
    )

    def update_cost(self):
        """
        Updates cost when a new ingredient is added,
        """
        self.cost = self.ingredientline.aggregate(
            Sum(
                'ingredientline_total'
            )
        )['ingredientline_total__sum'] or 0
        self.save()

    class Meta:
        ordering = ["recipeName"]

    def __str__(self):
        return str(self.recipeName)


class Ingredients(models.Model):
    """A Model To Create Ingredients For The Recipes"""

    recipe = models.ForeignKey(
        Recipe,
        null=False, blank=False,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Product,
        on_delete=models.
        SET_NULL,
        null=True,
        related_name="ingredients"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    ingredientline_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the ingredientline_total
        and update the cost.
        """
        if self.ingredient.weight > 0:
            self.ingredientline_total =  Decimal(
                self.ingredient.cost / self.ingredient.weight) * self.quantity
        elif self.ingredient.quantity > 0:
            self.ingredientline_total =  Decimal(
                self.ingredient.cost / self.ingredient.quantity) * self.quantity
        else:
            self.ingredientline_total =  Decimal(
                self.ingredient.cost / self.ingredient.liquid_vol) * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.ingredient)


class Method(models.Model):
    """A Model To Create Steps For The Recipe"""

    Recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    Steps = models.TextField()

    def __str__(self):
        return str(self.Steps)
