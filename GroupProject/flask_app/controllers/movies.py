from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

UPLOAD_FOLDER = 'flask_app/static/img/IMAGE_UPLOADS'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/browse')
def browse():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'user_id': session['user_id']
    }
    movies = Movie.getAllMovies()
    user = User.get_user_by_id(data)
    
    return render_template('browse.html',loggedUser= User.get_user_by_id(data), movies=movies)


@app.route('/addMovie')
def addmovie():
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template('addMovie.html',loggedUser= User.get_user_by_id(data))

@app.route('/createmovie', methods = ['POST'])
def create_movie():
    if 'user_id' not in session:
        return redirect('/logout')

    if not Movie.validate_movie(request.form):
        return redirect(request.referrer)

    if request.files['image'] is None:
        image= ''
        flash('Image is required', image)
    if request.files['image'] is not None:
        image = request.files['image']

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time += filename
        filename = time
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    data = {
        'title': request.form['title'],
        'director': request.form['director'],
        'cast': request.form['cast'],
        'length': request.form['length'],
        'genre1': request.form['genre1'],
        'genre2': request.form['genre2'],
        'releasedate': request.form['releasedate'],
        'description': request.form['description'],
        'image': filename,
        'users_id': session['user_id']
    }
    Movie.createMovie(data)
    return redirect('/')

@app.route('/showMovie/<int:id>')
def viewMovie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'movie_id': id,
        'user_id': session['user_id']
    }
    userFavoriteMovies = Movie.get_logged_user_favorite_movies(data)
    return render_template('showMovie.html', loggedUser= User.get_user_by_id(data), movie = Movie.get_movie_by_id(data), userFavoriteMovies=userFavoriteMovies)

@app.route('/addtoFav/<int:id>')
def addFavorite(id):
    data = {
        'movie_id': id,
        'user_id': session['user_id']
    }
    Movie.addtoFav(data)
    return redirect(request.referrer)

@app.route('/removefromFav/<int:id>')
def removeFavorite(id):
    data = {
        'movie_id': id,
        'user_id': session['user_id']
    }
    Movie.removefromFav(data)
    return redirect(request.referrer)

@app.route('/myFavorites')
def showfavorites():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'movie_id': id,
        'user_id': session['user_id']
    }
    movies = Movie.getAllMovies()
    favmovies = Movie.getFavoriteMovies(data)
    user = User.get_user_by_id(data)
    
    return render_template('myFavoriteMovies.html',loggedUser= User.get_user_by_id(data), movies=movies, favmovies=favmovies)

@app.route('/editmovie/<int:id>')
def editMovie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'movie_id': id,
        'user_id': session['user_id']
    }
    currentUser = User.get_user_by_id(data)
    if not session['user_id'] == currentUser['id']:
        flash('You do not have the facilities for that big man.', 'noAccessError')
        return redirect('/dashboard')   
    return render_template('editMovie.html', loggedUser= User.get_user_by_id(data),movie = Movie.get_movie_by_id(data) )

@app.route('/update/<int:id>', methods = ['POST'])
def updateMovie(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Movie.validate_movie(request.form):
        return redirect(request.referrer)
    
    data = {
        'movie_id' : id
    }

    data1 ={
        'title': request.form['title'],
        'director': request.form['director'],
        'cast': request.form['cast'],
        'length': request.form['length'],
        'genre1': request.form['genre1'],
        'genre2': request.form['genre2'],
        'releasedate': request.form['releasedate'],
        'description': request.form['description'],
        'user_id': session['user_id'],
        'movie_id':id
    }

    currentUser = User.get_user_by_id(data)

    if not session['user_id'] == currentUser['id']:
        flash('You do not have the facilities for that big man.', 'noAccessError')
        return redirect('/dashboard')   

    Movie.update_movie(data1)

    return redirect('/') 

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'movie_id': id,
        'user_id': session['user_id']
    }
    currentUser = User.get_user_by_id(data)
    if not session['user_id'] == currentUser['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    Movie.delete(data)
    return redirect(request.referrer)