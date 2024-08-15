from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes_home, name='recipes'),
    path('all/', views.all_recipes, name='recipes_all'),
    path('add/', views.add_recipe, name='recipe_add'),
    path('recipe_view/<pk>/', views.view_recipe, name='recipe_view'),
    path('edit_recipe/<pk>/update/', views.edit_recipe, name="recipe_edit"),
    path('recipe_delete/<pk>/delete/', views.recipe_delete, name="recipe_delete"),
    path('ingredients/<pk>/', views.ingredients, name='ingredients'),
    path('htmx/add_ingredient/', views.add_ingredient, name='ingredient_add'),
    path('htmx/ingredient_details/<pk>/',
         views.ingredient_details, name="ingredient_details"),
    path('htmx/update_ingredient/<pk>/update/',
         views.update_ingredient, name="update_ingredient"),
    path('htmx/delete_ingredient/<pk>/delete/',
         views.delete_ingredient, name="delete_ingredient"),
    path('method/<pk>/', views.method, name='method'),
    path('htmx/add_step/', views.add_step, name='step_add'),
    path('htmx/step_details/<pk>/update/',
         views.step_details, name="step_details"),
    path('htmx/update_step/<pk>/update/',
         views.update_step, name="update_step"),
    path('htmx/delete_step/<pk>/delete/',
         views.delete_step, name="delete_step"),
]
