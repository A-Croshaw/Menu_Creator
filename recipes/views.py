from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Recipe, RecipeCategory, RecipeSubcategory, Ingredients, Method
from .forms import RecipeForm, IngredientsForm, MethodForm


def recipes_home(request):
    """
    A view to render recipe manager
    """
    recipesubcategories = RecipeSubcategory.objects.all()
    recipecategories = RecipeCategory.objects.all()
    context={
        'recipesubcategories':recipesubcategories,
        'recipecategories':recipecategories,
    }
    template = 'recipes/recipes_home.html'
    return render(request, template, context)


def all_recipes(request):
    """
    A view to render all recipes with sorting and searching
    """
    recipes = Recipe.objects.all()
    recipecategories = None
    query = None
    sort = None
    direction = None
    recipesubcategories = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'recipeName':
                sortkey = 'lower_recipeName'
                recipes = recipes.annotate(lower_recipeName=Lower('recipeName'))
            if sortkey == 'recipecategory':
                sortkey = 'recipecategory__recipecategory'
            if sortkey == 'recipesubcategory':
                sortkey = 'recipesubcategory__recipesubcategory'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            recipes = recipes.order_by(sortkey)

        if 'recipecategory' in request.GET:
            recipecategories = request.GET['recipecategory'].split(',')
            recipes = recipes.filter(
                recipecategory__recipecategory__in=recipecategories)
            recipecategories = RecipeCategory.objects.filter(
                recipecategory__in=recipecategories)

        if 'recipesubcategory' in request.GET:
            recipesubcategories = request.GET['recipesubcategory'].split(',')
            recipes = recipes.filter(
                recipesubcategory__recipesubcategory__in=recipesubcategories)
            recipesubcategories = RecipeSubcategory.objects.filter(
                recipesubcategory__in=recipesubcategories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No recipes with that criteria")
                return redirect(reverse('recipes_all'))

            queries = Q(recipeName__icontains=query)
            recipes = recipes.filter(queries)

    current_sorted = f'{sort}_{direction}'
    template = 'recipes/recipes_all.html'
    context = {
        'recipes': recipes,
        'search_term': query,
        'sorted_recipecategories': recipecategories,
        'sorted_recipesubcategories': recipesubcategories,
        'current_sorted': current_sorted
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.add_recipe", raise_exception=True)
def add_recipe(request):
    """
    Add Recipe function
    """
    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only add recipes.')
        return redirect(reverse('home'))

    form = RecipeForm(request.POST or request.FILES)

    if request.method == "POST":
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.recipe = recipe
            recipe.save()
            messages.success(request, 'Recipe Added Successfully!')
            return redirect("ingredients", pk=recipe.id)
        else:
            return render(request,
                          "recipes/recipe_add.html",
                          context={
                              "form": form
                          })

    template = "recipes/recipe_add.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def view_recipe(request, pk):
    """View full Recipie"""
    recipe = Recipe.objects.get(id=pk)
    step = Method.objects.filter(recipe=recipe)
    ingredient = Ingredients.objects.filter(recipe=recipe)

    template = "recipes/recipe_view.html"
    context = {
        "recipe": recipe,
        "step": step,
        "ingredient": ingredient
    }
    return render(request, template, context,)


@login_required
@permission_required("recipes.recipe_edit", raise_exception=True)
def edit_recipe(request, pk):
    """Updates Recipe Fields"""
    recipe = Recipe.objects.get(id=pk)
    form = RecipeForm(request.POST or None, instance=recipe)
    step = Method.objects.filter(recipe=recipe)
    ingredient = Ingredients.objects.filter(recipe=recipe)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully!')
        return redirect("ingredients", pk=recipe.id)

    template = "recipes/recipe_edit.html"
    context = {
        "form": form,
        "recipe": recipe,
        "ingredient": ingredient,
        "step": step,
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.recipe_delete", raise_exception=True)
def recipe_delete(request, pk):
    """ Delete recipe """
    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only delete recipes.')
        return redirect(reverse('recipes'))

    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        recipe.delete()
        messages.success(
            request, f'{recipe.recipeName} has been delete successfully!')
        return redirect(reverse('recipes'))

    template = "recipes/recipe_delete.html"
    context = {
        'recipe': recipe,
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Ingredients
@login_required
@permission_required("recipes.ingredients", raise_exception=True)
def ingredients(request, pk):
    """Creates Ingredient Fields And Add More Enterys"""
    recipe = Recipe.objects.get(id=pk)
    step = Method.objects.filter(recipe=recipe)
    ingredient = Ingredients.objects.filter(recipe=recipe)
    form = IngredientsForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            messages.success(request, 'Ingredient Added Successfully!')
            return redirect("ingredient_details", pk=ingredient.id)
        else:
            return render(request,
                          "includes/ingredient_add.html",
                          context={
                              "form": form
                          })

    template = "recipes/ingredients.html"
    context = {
        "form": form,
        "recipe": recipe,
        "step": step,
        "ingredient": ingredient,
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.add_ingredients", raise_exception=True)
def add_ingredient(request):
    """Renders The Form Add Extra Ingredients"""
    form = IngredientsForm()
    template = "includes/ingredient_add.html"
    context = {
        "form": form
    }
    return render(request, template, context)


def ingredient_details(request, pk):
    """Displays Ingredient Fields After Being Added"""
    ingredient = get_object_or_404(Ingredients, id=pk)
    template = "includes/ingredient_details.html"
    context = {
        "ingredient": ingredient
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.update_ingredient", raise_exception=True)
def update_ingredient(request, pk):
    """Updates Ingredient Fields"""
    ingredient = Ingredients.objects.get(id=pk)
    form = IngredientsForm(
        request.POST or None,
        instance=ingredient
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfull!')
        return redirect("ingredient_details", pk=ingredient.id)

    template = "includes/ingredient_add.html"
    context = {
        "form": form,
        "ingredient": ingredient
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.delete_ingredient", raise_exception=True)
def delete_ingredient(request, pk):
    """Deletes Ingredient Fields"""
    ingredient = get_object_or_404(Ingredients, id=pk)

    if request.method == "POST":
        ingredient.delete()
        messages.success(request, 'Ingredient Deleted')
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


# ------------------------------------------------------------------ Method
@login_required
@permission_required("recipes.ingredients", raise_exception=True)
def method(request, pk):
    """Creates Step Fields And Add More Enterys"""
    recipe = Recipe.objects.get(id=pk)
    step = Method.objects.filter(recipe=recipe)
    ingredient = Ingredients.objects.filter(recipe=recipe)
    form = MethodForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe
            step.save()
            messages.success(request, 'Step Added Successfully!')
            return redirect("step_details", pk=step.id)
        else:
            return render(request,
                          "includes/step_add.html",
                          context={
                              "form": form
                          })

    template = "recipes/method.html"
    context = {
        "form": form,
        "recipe": recipe,
        'ingredient':ingredient,
        "step": step
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.add_step", raise_exception=True)
def add_step(request):
    """Renders The Form Add Extra Step"""
    form = MethodForm()
    template = "includes/step_add.html"
    context = {
        "form": form
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.update_step", raise_exception=True)
def update_step(request, pk):
    """Updates Step Fields"""
    step = Method.objects.get(id=pk)
    form = MethodForm(request.POST or None, instance=step)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully!')
        return redirect("step_details", pk=step.id)

    template = "includes/step_add.html"
    context = {
        "form": form,
        "step": step
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.step_details", raise_exception=True)
def step_details(request, pk):
    """Displays Step Fields for updating"""
    step = get_object_or_404(Method, id=pk)
    template = "includes/step_details.html"
    context = {
        "step": step
    }
    return render(request, template, context)


@login_required
@permission_required("recipes.delete_step", raise_exception=True)
def delete_step(request, pk):
    """Deletes Step Fields"""
    step = get_object_or_404(Method, id=pk)

    if request.method == "POST":
        step.delete()
        messages.success(request, 'Step Deleted')
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )
