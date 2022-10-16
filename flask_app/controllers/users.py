import re
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model.user import User
from flask_app.model.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def display():
    if session['user'] > 0:
        user_id = session['user']
        return redirect(f'/welcome/{user_id}')
    else:
        return render_template("login.html")

@app.route('/create', methods=['POST'])
def create_user():
    data = {
        "fname" : request.form['fname'],
        "lname" : request.form['lname'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "password2" : request.form['password2']
    }
    if not User.validate_user(data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "fname" : request.form['fname'],
        "lname" : request.form['lname'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.createuser(data)
    session['user'] = user_id
    return redirect(f'/welcome/{user_id}')

@app.route('/welcome/<int:id>')
def welcome(id):
    if session['user'] != id:
        return redirect('/logout')
    user = User.getuser(id)
    recipes = Recipe.getrecipes()
    return render_template("welcome.html", user = user, recipes = recipes)

@app.route('/login', methods = ['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    user = user_in_db.id
    session['user']= user_in_db.id
    return redirect(f'/welcome/{user}')

@app.route('/addrecipe')
def add():
    return render_template("addrecipe.html")

@app.route('/logout')
def logout():
    session['user'] = 0
    return redirect('/')

@app.route('/createrecipe', methods=['POST'])
def createrecipe():
    under = request.form['pick']
    if under == "yes":
        under = 1
    elif under == "no":
        under = 2
    data = {
        "name" : request.form['name'],
        "desc" : request.form['desc'],
        "instr" : request.form['instr'],
        "date" : request.form['date'],
        "under" : under,
        "user_id" : session['user']
    }
    if not Recipe.validate_recipe(data):
        return redirect('/addrecipe')
    user_id = session['user']
    Recipe.addrecipe(data)
    return redirect(f'/welcome/{user_id}')

@app.route('/view/<int:id>')
def view(id):
    if session['user'] < 1:
        return redirect('/')
    recipes = Recipe.viewrecipe(id)
    user = User.getuserbyrecipe(id)
    return render_template("view.html", recipes = recipes, user = user)

@app.route('/back')
def back():
    user_id = session['user']
    return redirect(f'/welcome/{user_id}')

@app.route('/edit/<int:id>')
def edit(id):
    recipe = Recipe.viewrecipe(id)
    if session['user'] != recipe.user_id:
        return redirect('/')
    return render_template("edit.html", recipe = recipe)
    
@app.route('/updaterecipe/<int:id>', methods=['POST'])
def update(id):
    if request.form['pick'] == "yes":
        under = 1
    elif request.form['pick'] == "no":
        under = 2
    data = {
        "id":id,
        "name":request.form['name'],
        "desc":request.form['desc'],
        "instr":request.form['instr'],
        "under":under,
        "updated_at":request.form['date']
    }
    if not Recipe.validate_recipe(data):
        return redirect(f'/edit/{id}')
    Recipe.update(data)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    Recipe.delete(id)
    return redirect('/')