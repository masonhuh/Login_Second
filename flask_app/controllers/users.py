from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt

from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/register', methods=['POST'])
def register_user():

    if User.validate_registration(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        User.create_user(data)
        flash("Account has been created. Please login.")

    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login_user():

    users = User.get_user_by_email(request.form)

    if len(users) != 1:
        flash('Email is incorrect.')
        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect.')
        return redirect('/')

    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['email'] = user.email
    return redirect('/success')

@app.route('/success')
def success():
    if 'user_id' not in session:
        flash('Please log in to view page.')
        return redirect('/')

    return render_template('success.html', user_id = session['user_id'], email = session['email'], first_name = session['first_name'])

@app.route('/users/logout')
def logout():
    session.clear()
    flash("You've logged out - bye bye. Log back in to continue.")
    return redirect('/')