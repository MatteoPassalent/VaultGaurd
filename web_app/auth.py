from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import hashlib

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["POST"])
def login():
    """
    -------------------------------------------------------
    Handles POST requests for /login end point. Retrieves
    user info from HTTP request. Attempts to find matching
    user from database. Checks for correct password.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Redirects to Home end point if valid login
        Returns to login page if not valid login
    -------------------------------------------------------
    """

    req_email = request.form.get("email")
    req_password = request.form.get("password")

    req_email = hashlib.sha256(req_email.encode()).hexdigest()

    user = User.query.filter_by(email=req_email).first()
    if user:
        if check_password_hash(user.password, req_password):
            login_user(user, remember=True)

            return redirect(url_for("views.home"))

        else:
            flash("Incorrect password, try again.")
    else:
        flash("User does not exist")

    return render_template("login.html", user=current_user)


@auth.route("/login", methods=["GET"])
def login_g():
    """
    -------------------------------------------------------
    Handles GET requests for /login end point.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Renders login page
    -------------------------------------------------------
    """

    return render_template("login.html")


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    -------------------------------------------------------
    Handles /logout endpoint. Uses logout_user from
    flask_login.
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Redirects to login page route
    -------------------------------------------------------
    """
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["POST"])
def sign_up():
    """
    -------------------------------------------------------
    Handles POST requests for /sign-up end point. Retrieves
    user info from HTTP request. Checks if user already
    exists in database. Checks for validity of user info.
    Creates new instance of User class and adds to db.
    Logs new user in.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Redirects to Home end point if valid new user
        Returns to sign-up page if not valid login
    -------------------------------------------------------
    """
    email = request.form.get("email")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    email = hashlib.sha256(email.encode()).hexdigest()

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email in use.")
    elif len(email) < 4:
        flash("Email must be at least 5 characters")
    elif password1 != password2:
        flash("Passwords do not match")
    elif len(password1) < 7:
        flash("Password must be at least 7 characters.")
    else:
        new_user = User(
            email=email,
            password=generate_password_hash(password1, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)


@auth.route("/sign-up", methods=["GET"])
def sign_up_g():
    """
    -------------------------------------------------------
    Handles GET requests for /sing-up end point.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Renders sing-up page
    -------------------------------------------------------
    """
    return render_template("sign_up.html")
