##from django.shortcuts import render


from django.views.generic import TemplateView

class Recipes(TemplateView):

    template_name = 'recipes/recipes.html'
