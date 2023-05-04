from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Account
import json

# creates blueprint object named views
# Note: Blueprint holds multiple routes inside, can be used like an individual flask app.
views = Blueprint("views", __name__)


# Handles http get request
# Note: login_required checks if current_user is None. If it is then user is redirected to endpoint set in init ("login_manager.login_view = 'auth.login'")
@views.route("/", methods=["GET"])
@login_required
def home():
    """
    -------------------------------------------------------
    Handles GET requests for / endpoint.
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Renders home page
    -------------------------------------------------------
    """
    return render_template("home.html", user=current_user)


@views.route("/", methods=["POST"])
@login_required
def add_account():
    """
    -------------------------------------------------------
    Handles POST requests for / endpoint. Adds new account.
    Retrieves new account info from user. Checks for
    validity. Creates a new instance of Account class and
    adds to db.
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Redirects to home page route
    -------------------------------------------------------
    """
    # Current user returns authenticated if logged in.
    # Note user.is_aunthenticated is used for nav bar in base.html
    # Retrieves info from user
    if request.method == "POST":
        AccountTitle = request.form.get("accountTitle")
        UserName = request.form.get("userName")
        Email = request.form.get("email")
        Password = request.form.get("password")
        Additional = request.form.get("additional")

        # Checks validity
        if len(AccountTitle) < 1:
            flash("Account Title required", category="error")
        elif len(AccountTitle) > 20:
            flash("Account Title Too Long", category="error")
        elif len(UserName) > 21:
            flash("Username is too long", category="error")
        elif len(Password) > 50:
            flash("Password is too long", category="error")
        elif len(Email) > 35:
            flash("Email is too long", category="error")
        elif len(Additional) > 130:
            flash("Additional Info is too long", category="error")
        else:
            # Creates a new instance of account and adds to database
            new_Account = Account(
                AccountTitle=AccountTitle,
                UserName=UserName,
                Email=Email,
                Password=Password,
                Additional=Additional,
                user_id=current_user.id,
            )
            db.session.add(new_Account)
            db.session.commit()
            flash("Account added!", category="success")

    # Redirects back to home page route
    # Note: Home page will now display new account
    return redirect(url_for("views.home"))


# Note: Called from DeleteAccount js function
@views.route("/delete-account", methods=["POST"])
def delete_account():
    """
    -------------------------------------------------------
    Handles POST requests for /delete-account endpoint.
    Retrieves accountId for account to be deleted. Queries
    db for account with matching id. Deletes account.
    Use:
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        None
    -------------------------------------------------------
    """
    # Retrieves accountId from account to be deleted
    account = json.loads(request.data)
    account_id = account["accountId"]

    # Queries database for account with matching id
    # Note: Account class has .query method due to inheritance from db.Model
    account = Account.query.get(account_id)
    # If account is found and the user who created account matches the user deleting it then it is deleted from db
    if account:
        if account.user_id == current_user.id:
            db.session.delete(account)
            db.session.commit()

    # Note: Homepage '/' is returned to in DeleteAccount function in js. Need to return jsonify({}) to avoid error message
    return jsonify({})
