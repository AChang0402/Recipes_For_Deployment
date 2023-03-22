from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe

@app.route('/recipes')
def all_recipes():
    if 'email' not in session:
        return redirect('/')
    all_recipes = Recipe.get_all_recipes()
    current_user = User.get_one_by_email({'email':session['email']})
    return render_template('recipes.html', all_recipes = all_recipes, current_user=current_user)

@app.route('/recipes/new')
def add_recipe():
    if 'email' not in session:
        return redirect('/')
    return render_template('addrecipe.html')

@app.route('/recipes/new/create', methods=['post'])
def create_recipe():
    if 'email' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    recipe_data = {
        ** request.form,
        'user_id':session['id']
    }
    new_recipe_id = Recipe.create_recipe(recipe_data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'email' not in session:
        return redirect('/')
    recipe = Recipe.get_recipe({'id':id})
    current_user = User.get_one_by_email({'email':session['email']})
    print(recipe.under)
    return render_template("viewrecipe.html", recipe=recipe, current_user=current_user)

@app.route('/recipes/edit/<int:id>')
def change_recipe(id):
    if 'email' not in session:
        return redirect('/')
    recipe = Recipe.get_recipe({'id':id})
    return render_template("editrecipe.html", recipe=recipe)

@app.route('/recipes/edit/<int:id>/change', methods=['post'])
def submit_changes(id):
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/edit/'+str(id))
    recipe_data = {
        ** request.form,
        'id':id
    }
    Recipe.edit_recipe(recipe_data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    Recipe.delete_recipe({'id':id})
    return redirect('/recipes')
