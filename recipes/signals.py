from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Ingredients

@receiver(post_save, sender=Ingredients)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update Cost on ingredientline update/create
    """
    instance.recipe.update_cost()

@receiver(post_delete, sender=Ingredients)
def update_on_delete(sender, instance, **kwargs):
    """
    Update Cost on ingredientline delete
    """
    instance.recipe.update_cost()