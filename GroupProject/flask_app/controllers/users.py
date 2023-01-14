from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/logout')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')

@app.route('/loginPage')
def loginPage():    
    if 'user_id' in session:
        return redirect('/')
    return render_template('loginRegistration.html')

@app.route('/createUser', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    if User.get_user_by_email(request.form):
        flash('This email already exists, try another!', 'email')
        return redirect(request.referrer)
    data = {        
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.createUser(data)
    flash('You created the user succesfully! You can now use it to log in!', 'signUpSuccessful')
    return redirect(request.referrer)

@app.route('/login', methods=['POST'])
def login():    
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)
    if not User.get_user_by_email(data):
        flash('This email does not exist.', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    # allPrograms = Program.getAllProgramsFromUser(data)
    # userVotedPies = User.get_logged_user_voted_pies(data)
    # , pies= Pie.getAllPiesFromUser(data),userVotedPies=userVotedPies
    return render_template('dashboard.html',loggedUser= User.get_user_by_id(data))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template('Profile.html',loggedUser= User.get_user_by_id(data))

@app.route('/editProfile/<int:id>')
def editUser(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'user_id': id,
        'user_id': session['user_id']
    }
    currentUser = User.get_user_by_id(data)
    if not session['user_id'] == currentUser['id']:
        flash('You do not have the facilities for that big man.', 'noAccessError')
        return redirect('/dashboard')   
    return render_template('editprofile.html', loggedUser= User.get_user_by_id(data))

@app.route('/update/<int:id>', methods = ['POST'])
def updateUser(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_edit_user(request.form):
        return redirect(request.referrer)
    
    data = {
        'user_id' : id
    }

    data1 ={
        "firstname" : request.form["firstname"],
        "lastname" : request.form["lastname"],
        "password" : request.form["password"],
        'user_id': session['user_id'],
        'user_id':id
    }

    currentUser = User.get_user_by_id(data)

    if not session['user_id'] == currentUser['id']:
        flash('You do not have the facilities for that big man.', 'noAccessError')
        return redirect('/dashboard')   

    User.update_user(data1)

    return redirect('/') 

