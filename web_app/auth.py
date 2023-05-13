from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Note: Application is stateful due to flask-login keeping user data in server session

# creates blueprint object named auth
# Note: Blueprint holds multiple routes inside, can be used like an individual flask app.
auth = Blueprint("auth", __name__)


# same as app.route but for blueprint, handles both GET and POST, only needs to render the login html template
@auth.route("/login", methods=["POST"])
def login():
    """
    -------------------------------------------------------
    Handles POST requests for /login end point. Retrieves
    user info from HTTP request. Attempts to find matching
    user from database. Checks for correct password.
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Redirects to Home end point if valid login
        Returns to login page if not valid login
    -------------------------------------------------------
    """

    # Retrieves input from user
    req_email = request.form.get("email")
    req_password = request.form.get("password")
    # Queries database, if an email in database matches email from user then returns user, else None
    user = User.query.filter_by(email=req_email).first()
    if user:
        # Uses check_password_hash to check password from POST request against user password from db with corresponding email
        if check_password_hash(user.password, req_password):
            # Uses login_user. remeber = True keeps the user logged in if app is opened again in the same browser (session managment not caching)
            login_user(user, remember=True)

            # Note: Using url_for instead of having to hardcode the link to the home page.
            return redirect(url_for("views.home"))

        else:
            flash("Incorrect password, try again.")
    else:
        flash("User does not exist")

    # Renders login page again if login falied
    # Note: Current user is default anonymous user if not logged in
    return render_template("login.html", user=current_user)


@auth.route("/login", methods=["GET"])
def login_g():
    """
    -------------------------------------------------------
    Handles GET requests for /login end point.
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Renders login page
    -------------------------------------------------------
    """
    return render_template("login.html", user=current_user)


# Note: login_required checks if current_user is None. If it is then user is redirected to endpoint set in init ("login_manager.login_view = 'auth.login'")
@auth.route("/logout")
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
    # Note: Logs out current user and cleans remeber if needed.
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
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Redirects to Home end point if valid new user
        Returns to sign-up page if not valid login
    -------------------------------------------------------
    """
    # Retrieves info from user
    email = request.form.get("email")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    # Queries db for user with matching email,
    # Note: need .first() because otherwise user variable will never be None even if not found
    user = User.query.filter_by(email=email).first()

    # Checks valididty of user info
    if user:
        flash("Email in use.")
    elif len(email) < 4:
        flash("Email must be at least 5 characters")
    elif password1 != password2:
        flash("Passwords do not match")
    elif len(password1) < 7:
        flash("Password must be at least 7 characters.")
    else:
        # Creates new instance of user class if all requirements are met
        # Note: Uses hashing for password, sha256 is a hashing algorithm
        new_user = User(
            email=email,
            password=generate_password_hash(password1, method="sha256"),
        )
        # Adds new user to database
        db.session.add(new_user)
        db.session.commit()
        # Logs user in with flask login
        login_user(new_user, remember=True)
        # Redirects to home page
        return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)


@auth.route("/sign-up", methods=["GET"])
def sign_up_g():
    """
    -------------------------------------------------------
    Handles GET requests for /sing-up end point.
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Renders sing-up page
    -------------------------------------------------------
    """
    return render_template("sign_up.html", user=current_user)
