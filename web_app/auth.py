from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User

# hashes password so it cannot be seen in normal text. Hashing functions convert text to hash but have no inverse (no hash to text)
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Blueprint holds multiple routes inside, flash is a message box on the form, form.get is unrelated get method
# creates blueprint object (mini flask app)
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    # POST only if signing in, not loading page
    if request.method == "POST":
        # gets input from user using request module
        email = request.form.get("email")
        password = request.form.get("password")
        # queries data base an email in database matches email from user then returns user and checks for correct password
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                # uses flask module: login_user to log in this user found by query and stores them if in the same browser
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("User does not exist", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
# mod from flask that makes sure you cant access page unless logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_Name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email in use.", category="error")
        elif len(email) < 4:
            flash("First name must be at least 5 characters", category="error")
        elif len(first_Name) < 2:
            flash("First name must be at least 3 characters", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            # sha256 is a hashing algorithm
            new_user = User(
                email=email,
                first_Name=first_Name,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(new_user, remember=True)
            # redirects once user is logged. views is name of blueprint with function home which renders template for home page. Therefore 'views.home'
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
