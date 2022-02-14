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
    Function for recipes app route, retrieves
    """
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Function for register app route. Registers new users with db.
    """
    if request.method == 'POST':
        #check if username or email already exists in db
        existing_username = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})
        existing_email = mongo.db.users.find_one(
            {'email': request.form.get('email').lower()})

        if existing_username:
            flash('Username already exists')
            return

        if existing_email:
            flash('Email already registered')
            return
                      
        register_user = {
            'username': request.form.get('username').lower(),
            'password': generate_password_hash(request.form.get('password')),
            'first_name': request.form.get('first_name').lower(),
            'last_name': request.form.get('last_name').lower(),
            'email': request.form.get('email').lower(),
        }
        mongo.db.users.insert_one(register_user)

    return redirect(url_for('get_recipes'))



if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "127.0.0.1"),
            port=int(os.environ.get("PORT", 5000)),
            debug=True)
