# website/auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # Redirect logged-in users from login page
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip() 
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email or password, please try again.', category='error') # More generic error for security
        else:
            flash('Incorrect email or password, please try again.', category='error') # More generic error
            
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required # Ensure only logged-in users can logout
def logout():
    logout_user()
    flash('You have been logged out.', category='info') # Use 'info' for a neutral message
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated: # Redirect logged-in users from signup page
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first_name', '').strip()
        password1 = request.form.get('password1', '').strip()
        password2 = request.form.get('password2', '').strip()

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please use a different one.', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif not "@" in email or not "." in email: # Basic email format validation
            flash('Please enter a valid email address.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be at least 2 characters long.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)