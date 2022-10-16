from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.model import recipe
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id= data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes=[]


    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['fname']) < 3:
            flash("First Name should be more than 2 characters.")
            is_valid = False
        if len(data['lname']) < 3:
            flash("Last Name should be more than 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password should be at least 8 characters.")
            is_valid = False
        if not data['password2'] == data['password']:
            flash('Passwords do not match.')
            is_valid = False
        return is_valid

    @classmethod
    def createuser(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL('userrecipe').query_db(query, data)
        return result


    @classmethod
    def getuser(cls, id):
        data = {"id":id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('userrecipe').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('userrecipe').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def getuser_recipe(cls, id):
        data = {"id":id}
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE user_id = %(id)s;"
        result = connectToMySQL('userrecipe').query_db(query, data)
        if len(result) > 0:
            users = cls(result[0])
            for row in result:
                recipe_data={
                    "id" : row['recipes.id'],
                    "name": row['name'],
                    "description" : row['description'],
                    "instructions" : row['instructions'],
                    "under" : row['under'],
                    "user_id": row['user_id'],
                    "created_at" : row['recipes.created_at'],
                    "updated_at" : row['recipes.updated_at']
                }
                users.recipes.append(recipe.Recipe(recipe_data))
                return users
        else:
            data = {"id":id}
            query = "SELECT * FROM users WHERE id = %(id)s;"
            result = connectToMySQL('userrecipe').query_db(query, data)
            return cls(result[0])
        
    @classmethod
    def getuserbyrecipe(cls, id):
        data = {"id":id}
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL('userrecipe').query_db(query, data)
        users = cls(result[0])
        return users