from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = user_login()

        if response == True:
            flash('Logged In Succesfully', category='success')
            return redirect(url_for('views.home'))
        else:
            flash(response, category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        response = user_signup()
        
        if response == True:
            flash('Account Created. Please Login', category='success')
            return redirect(url_for('auth.login'))
        else:
            flash(response, category='error')

    return render_template('sign_up.html', user=current_user)

# functions
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return True
        else:
            return 'Incorect Password'
    else:
        return 'Not Registared'

def user_signup():
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 =request.form.get('password2')
    first_name = request.form.get('firstName')

    user = User.query.filter_by(email=email).first()
    if user:
        return 'Email already registared'
    elif not validate_email(email):
        return 'Invalid Email'
    elif len(first_name) < 1:
        return 'Type in your Name'
    elif len(password1) < 8:
        return 'Password is too small, Minimum length 8'
    elif not (password1 == password2):
        return 'Passwords didn\'t match'
    else:
        creat_user(email, password1, first_name)
        return True

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def creat_user(email, password1, first_name):
    password = generate_password_hash(password1, method='sha256')
    new_user = User(email=email, password=password, first_name=first_name)
    db.session.add(new_user)
    db.session.commit()
