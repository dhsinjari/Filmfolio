from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Movie:
    db_name='filmfolio'
    def __init__(self,data):
        self.id = data['id'],
        self.title = data['title'],
        self.length = data['length'],
        self.genre1 = data['genre1'],        
        self.genre2 = data['genre2'],
        self.releasedate = data['releasedate'],
        self.description = data['description'],
        self.cast = data['cast'],
        self.director = data['director'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def getAllMovies(cls):
        query = 'SELECT * FROM movies;'
        results = connectToMySQL(cls.db_name).query_db(query)
        movies = []
        for row in results:
            movies.append(row)
        return movies
    
    @classmethod
    def createMovie(cls,data):
        query = 'INSERT INTO movies (title,length,genre1,genre2,releasedate,description,users_id,image,director,cast) VALUES (%(title)s,%(length)s,%(genre1)s,%(genre2)s,%(releasedate)s,%(description)s,%(users_id)s,%(image)s,%(cast)s,%(director)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_movie_by_id(cls,data):
        query = 'SELECT * FROM movies WHERE id = %(movie_id)s ;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
    
    @classmethod
    def update_movie(cls,data1):
        query = 'UPDATE movies SET title=%(title)s, length=%(length)s, genre1=%(genre1)s,genre2=%(genre2)s,releasedate=%(releasedate)s,description=%(description)s,image=%(image)s,cast=%(cast)s,director=%(director)s WHERE id=%(movie_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data1)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM movies WHERE id = %(movie_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_logged_user_favorite_movies(cls, data):
        query = 'SELECT movies_id  as id FROM favorites LEFT JOIN users on favorites.users_id = users.id WHERE users_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        FavoriteMovies = []
        for row in results:
            FavoriteMovies.append(row['id'])
        return FavoriteMovies    

    @classmethod
    def getFavoriteMovies(cls, data):
        query = 'SELECT * from favorites LEFT JOIN movies on favorites.movies_id = movies.id WHERE favorites.users_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        FavoriteMovies = []
        for row in results:
            FavoriteMovies.append(row)
        return FavoriteMovies

    @classmethod
    def addtoFav(cls, data):
        query= 'INSERT INTO favorites (movies_id, users_id) VALUES ( %(movie_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removefromFav(cls, data):
        query= 'DELETE FROM favorites WHERE movies_id = %(movie_id)s and users_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_movie(movie):
        is_valid = True 
        if len(movie['title']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False

        if len(movie['length']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False

        if len(movie['genre1']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False

        if len(movie['genre2']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False
        
        if len(movie['releasedate']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False

        if len(movie['description']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False
        return is_valid