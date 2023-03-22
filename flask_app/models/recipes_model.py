from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users_model

DATABASE = "recipes_schema"

class Recipe():
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes=[]
        for row in range(len(results)):
            print(row)
            this_recipe = cls(results[row])
            print(this_recipe)
            posted_by = {
                'id' : results[row]['users.id'],
                'first_name' : results[row]['first_name'],
                'last_name' : results[row]['last_name'],
                'email' : results[row]['email'],
                'password' : results[row]['password'],
                'created_at' : results[row]['users.created_at'],
                'updated_at' : results[row]['users.updated_at']
            }
            this_recipe.user = users_model.User(posted_by)
            all_recipes.append(this_recipe)
        return all_recipes
    
    @classmethod
    def create_recipe(cls, data):
        query = """
                INSERT INTO recipes (user_id, name, under, description, instructions, date_made) 
                VALUES (%(user_id)s,%(name)s,%(under)s,%(description)s,%(instructions)s,%(date_made)s);
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_recipe(cls, data):
        query = """
                SELECT * from recipes LEFT JOIN users On user_id = users.id
                WHERE recipes.id=%(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query,data)
        one_recipe = cls(result[0])
        poster_data = {'email':result[0]['email']}
        posted_by = users_model.User.get_one_by_email(poster_data)
        one_recipe.posted_by = posted_by
        return one_recipe
    
    @classmethod
    def edit_recipe(cls, data):
        query = """
                UPDATE recipes
                SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under=%(under)s, date_made=%(date_made)s
                WHERE id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete_recipe(cls,data):
        query = """
                DELETE FROM recipes where id=%(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query,data)

    
    @staticmethod
    def validate_recipe(data):
        is_valid=True
        if len(data['name'])<3:
            flash("Name must contain at least 3 characters", "recipe")
            is_valid=False
        if len(data['description'])<3:
            flash("Description must contain at least 3 characters", "recipe")
            is_valid=False
        if len(data['instructions'])<3:
            flash("Instructions must contain at least 3 characters", "recipe")
            is_valid=False
        if len(data['date_made'])<1:
            flash("Date is required", "recipe")
            is_valid=False
        if 'under' not in data:
            flash("Over/Under 30 minutes selection is required", "recipe")
            is_valid=False
        return is_valid
        
