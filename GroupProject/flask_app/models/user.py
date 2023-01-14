from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name='filmfolio'
    def __init__(self,data):
        self.id = data['id'],
        self.firstname = data['firstname'],
        self.lastname = data['lastname'],
        self.email = data['email'],        
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def getAllUsers(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append(row)
        return users

    @classmethod
    def createUser(cls,data):
        query = 'INSERT INTO users (firstname,lastname,email,password) VALUES(%(firstname)s,%(lastname)s,%(email)s,%(password)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_id(cls,data):
        query = 'SELECT * FROM users WHERE users.id = %(user_id)s ;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]

    @classmethod
    def update_user(cls,data1):
        query = 'UPDATE users SET firstname=%(firstname)s, lastname=%(lastname)s, password=%(password)s WHERE id=%(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data1)

    # @classmethod
    # def get_logged_user_favorite_programs(cls, data):
    #     query = 'SELECT program_id as id FROM favorites LEFT JOIN users on favorites.user_id = users.id WHERE user_id = %(user_id)s;'
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     favPrograms = []
    #     for row in results:
    #         favPrograms.append(row['id'])
    #     return favPrograms

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['firstname']) < 3:
            flash("Name must be at least 3 characters.", 'firstname')
            is_valid = False
        if len(user['lastname']) < 3:
            flash("Last name be at least 3 characters.", 'lastname')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password be at least 8 characters.", 'passwordRegister')
            is_valid = False
        if user['confirmpassword'] != user['password']:
            flash("Password do not match!", 'passwordConfirm')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit_user(user):
        is_valid = True
        if len(user['firstname']) < 3:
            flash("Name must be at least 3 characters.", 'firstname')
            is_valid = False
        if len(user['lastname']) < 3:
            flash("Last name be at least 3 characters.", 'lastname')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password be at least 8 characters.", 'passwordRegister')
            is_valid = False
        if user['confirmpassword'] != user['password']:
            flash("Password do not match!", 'passwordConfirm')
            is_valid = False
        return is_valid        