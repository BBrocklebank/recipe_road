"""
Main app for site, linking Jinga templates to python functions.
Function then interact with MongoDB
"""


import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists('env.py'):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    """
    Retrieves all recipes.
    """
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registers new users with db.
    """
    if request.method == 'POST':
        #check if username or email exists in db
        existing_username = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})
        existing_email = mongo.db.users.find_one(
            {'email': request.form.get('email').lower()})

        password = request.form.get('password')
        password_check = request.form.get('password_check')

        if existing_username and existing_email:
            flash('Username and email already exist')
            return redirect(url_for('get_recipes'))

        elif existing_username:
            flash('Username already exists')
            return redirect(url_for('get_recipes'))

        elif existing_email:
            flash('Email already registered')
            return redirect(url_for('get_recipes'))

        elif password_check != password:
            flash('Passwords must match')
            return redirect(url_for('get_recipes'))

        register_user = {
            'username': request.form.get('username').lower(),
            'password': generate_password_hash(request.form.get('password')),
            'first_name': request.form.get('first_name').lower(),
            'last_name': request.form.get('last_name').lower(),
            'email': request.form.get('email').lower(),
        }
        mongo.db.users.insert_one(register_user)

        #Places user in session
        session['user'] = request.form.get('username').lower()
        flash('Registration Succesful!')
        return redirect(url_for('get_recipes', user=session['user']))

    return redirect(url_for('get_recipes'))


@app.route('/logout')
def logout():
    """
    Logout current session user.
    """
    # remove user from session cookies
    session.pop('user')
    return redirect(url_for('get_recipes'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs an existing user into their profile.
    """
    if request.method == 'POST':
        # Check if username exits in db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if check_password_hash(existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                name = request.form.get('username')
                flash(f'Welcome, {name}')
                return redirect(
                    url_for('get_recipes', username=session['user']))

            else:
                # invalid password match
                flash('Login: Incorrect Username and/or Password')
                return redirect(url_for('get_recipes'))

        else:
            # username doesn't exist
            flash('Login: Incorrect Username and/or Password')
            return redirect(url_for('get_recipes'))

    return redirect(url_for('get_recipes'))


@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
    """
    Grab session user's information from db
    """

    user = mongo.db.users.find_one({'username': session['user']}, {'password': 0})
    recipes = list(mongo.db.recipes.find())
     #Prevent users forcing to another profile
     # and if cookie error takes user to login page

    if session['user']:
        return render_template('profile.html', user=user, recipes=recipes)

    return redirect(url_for('login'))


@app.route('/edit_profile/<user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    """
    Update user profile details
    """

    if request.method == 'POST':

        #Existing User data
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

        username_exists = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})
        email_exists = mongo.db.users.find_one(
            {'email': request.form.get('email').lower()})

        edit_user = {}

        # Compares current user data with form data and/or then the database.
        # Sets dictionary value to be sent to db.

        # Do Username and Email need checking
        if user['email'] != request.form.get(
            'email').lower() and session['user'] != request.form.get('username').lower():

            if username_exists and email_exists:
                flash('Username and email already exist')
                return redirect(url_for('profile', user=user))

            elif username_exists:
                flash('Username already exists')
                return redirect(url_for('profile', user=user))

            elif email_exists:
                flash('Email already registered')
                return redirect(url_for('profile', user=user))

            else:
                edit_user = {
                'first_name': request.form.get('first_name').lower(),
                'last_name': request.form.get('last_name').lower(),
                'username': request.form.get('username').lower(),
                'email': request.form.get('email').lower()
                }
                session['user'] = request.form.get('username').lower()

        elif session['user'] != request.form.get('username').lower():

            if username_exists:
                flash('Username already exists')
                return redirect(url_for('profile', user=user))

            else:
                edit_user = {
                'first_name': request.form.get('first_name').lower(),
                'last_name': request.form.get('last_name').lower(),
                'username': request.form.get('username').lower()
                }
                session['user'] = request.form.get('username').lower()

        elif user['email'] != request.form.get('email').lower():

            if email_exists:
                flash('Email already registered')
                return redirect(url_for('profile', user=user))

            else:
                edit_user = {
                'first_name': request.form.get('first_name').lower(),
                'last_name': request.form.get('last_name').lower(),
                'email': request.form.get('email').lower()
                }

        else:
            edit_user = {
                'first_name': request.form.get('first_name').lower(),
                'last_name': request.form.get('last_name').lower(),
                }

        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": edit_user})

        flash('Update Succesful!')

    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return redirect(url_for('profile', user=user))


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    """
    Add recipe
    """
    if request.method == 'POST':

        recipe = {
            'cuisine_name': request.form.get('cuisine_name'),
            'recipe_name': request.form.get('recipe_name'),
            'recipe_description': request.form.get('recipe_description'),
            'serves': request.form.get('serves'),
            'requirements': request.form.get('requirements'),
            'ingredients': request.form.get('ingredients'),
            'steps1': request.form.get('steps1'),
            'steps2': request.form.get('steps2'),
            'steps3': request.form.get('steps3'),
            'steps4': request.form.get('steps4'),
            'steps5': request.form.get('steps5'),
            'created_by': session['user']
        }
        mongo.db.recipes.insert_one(recipe)
        flash('Recipe Successfully Added')
        return redirect(url_for('get_recipes'))

    recipe = mongo.db.recipes.find_one({'username': session['user']})
    cuisines = mongo.db.cuisines.find().sort('cuisine_name', 1)
    return render_template('add_recipe.html', cuisines=cuisines, recipe=recipe)


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    Update recipe
    """

    if request.method == 'POST':
        submit = {
            'cuisine_name': request.form.get('cuisine_name'),
            'recipe_name': request.form.get('recipe_name'),
            'recipe_description': request.form.get('recipe_description'),
            'serves': request.form.get('serves'),
            'requirements': request.form.get('requirements'),
            'ingredients': request.form.get('ingredients'),
            'steps1': request.form.get('steps1'),
            'steps2': request.form.get('steps2'),
            'steps3': request.form.get('steps3'),
            'steps4': request.form.get('steps4'),
            'steps5': request.form.get('steps5'),
            'created_by': session['user']
        }
        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$set": submit})
        flash("Recipe Successfully Updated")

    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    cuisines = mongo.db.cuisines.find().sort('cuisine_name', 1)
    return render_template('edit_recipe.html', recipe=recipe, cuisines=cuisines)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    """
    Delete recipe
    """
    mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
    flash('Recipe Successfully Deleted')
    return redirect(url_for('get_recipes'))


@app.route("/search", methods=['GET', 'POST'])
def search():
    """
    Search route
    """
    query = request.form.get('query')
    recipes = list(mongo.db.recipes.find({'$text': {'$search': query}}))
    return render_template("recipes.html", recipes=recipes)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", 5000)),
            debug=True)
