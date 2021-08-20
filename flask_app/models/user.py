import re

from flask_app import app 
from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection

class User():

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):

        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        result = MySQLConnection('login_schema').query_db(query, data)

        return result

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'

        results = MySQLConnection('login_schema').query_db(query, data)

        users = []

        for line in results:
            users.append(User(line))

        return users

    @staticmethod
    def validate_registration(data):

        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) < 2 or len(data['first_name']) > 255:
            is_valid = False
            flash('First name need to be at least 2 characters long.')

        if len(data['last_name']) < 2 or len(data['last_name']) > 255:
            is_valid = False
            flash('Last name need to be at least 2 characters long.')

        if len(User.get_user_by_email(data)) > 0:
            is_valid = False
            flash('Email is already in use.')

        if not email_regex.match(data['email']):
            is_valid = False
            flash('Email is not in correct format.')

        if len(data['email']) > 255:
            is_valid = False
            flash('Email is too long')

        if len(data['password']) < 8:
            is_valid = False
            flash('Password should be at least 8 characters long.')

        if not data['password'] == data['confirm_password']:
            is_valid = False
            flash('Password and confirm password do not macth')
        

        return is_valid