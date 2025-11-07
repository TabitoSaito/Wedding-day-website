from flask import render_template, redirect, url_for, current_app, flash
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user

from app.forms import LoginForm, RegisterForm
from app.extensions import db
from app.models import User
from app.constants import PROFILE_CHOICE

from . import auth_bp

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Load login form and process login logic

    - GET: render login form
    - POST: handel login logic and redirect to homepage
    """
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        # check if user is registered
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('auth.login'))
        # check for correct password
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('auth.login'))
        # redirect to homepage after successful login
        else:
            login_user(user)
            return redirect(url_for('main.home'))

    return render_template("login.html", form=form, current_user=current_user, cur_page="login")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """load register form and process register logic

    - GET: render register form
    - POST: handel register logic and redirect to homepage
    """
    form = RegisterForm()
    if form.validate_on_submit():

        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        # check if user already registered
        if user:
            flash("Du hast schon ein Konto! Melde dich an")
            return redirect(url_for('login'))

        # check security key
        if form.secret_key.data != current_app.config["SECRET_KEY_REGISTER"]:
            flash("Falscher Geheimcode")
            return redirect(url_for("register"))
        # check password repeat to avoid typo mistakes
        elif form.password_again.data != form.password.data:
            flash("Passwörter stimmen nicht überein")
            return redirect(url_for("register"))
        # hash password and add user to database
        else:
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            
            gender = random.choice(PROFILE_CHOICE)
            n = random.randint(1, 10)
            
            new_user = User(
                email=form.email.data,
                name=form.name.data,
                password=hash_and_salted_password,
                profile_pic=f"{gender}{n}"
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for("main.home"))

    return render_template("register.html", form=form, current_user=current_user, cur_page="register")

@auth_bp.route('/logout')
def logout():
    """logout current user and redirect to homepage
    """
    logout_user()
    return redirect(url_for('main.home'))