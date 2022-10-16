from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def addrecipe(cls, data):
        query= "INSERT INTO recipes (name, description, instructions, under, user_id, created_at, updated_at) VALUES (%(name)s, %(desc)s, %(instr)s, %(under)s, %(user_id)s, %(date)s, NOW());"
        result = connectToMySQL('userrecipe').query_db(query, data)
        return result

    @classmethod
    def viewrecipe(cls, recipe_id):
        data = {
            "recipe_id" : recipe_id
        }
        query = "SELECT * FROM recipes WHERE id = %(recipe_id)s;"
        result = connectToMySQL('userrecipe').query_db(query, data)
        recipe = cls(result[0])
        return recipe

    @classmethod
    def getrecipes(cls):
        query = "SELECT * FROM recipes"
        result = connectToMySQL('userrecipe').query_db(query)
        return result
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(desc)s, instructions=%(instr)s, under=%(under)s, updated_at=%(updated_at)s WHERE id = %(id)s;"
        result = connectToMySQL('userrecipe').query_db(query, data)
        return result

    @classmethod
    def delete(cls, id):
        data={"id":id}
        query= "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('userrecipe').query_db(query, data)
        return result

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name should be more than 2 characters.")
            is_valid = False
        if len(data['desc']) < 3:
            flash("Description should be more than 2 characters.")
            is_valid = False
        if len(data['instr']) < 8:
            flash("Instructions should be at least 8 characters.")
            is_valid = False
        return is_valid