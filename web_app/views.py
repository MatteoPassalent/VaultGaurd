from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Account
import json
from . import cipher_suite

views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
@login_required
def home():
    """
    -------------------------------------------------------
    Handles GET requests for / endpoint.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Renders home page
    -------------------------------------------------------
    """
    return render_template("home.html", user=current_user)


@views.route("/add-account", methods=["POST"])
@login_required
def add_account():
    """
    -------------------------------------------------------
    Handles POST requests for / endpoint. Adds new account.
    Retrieves new account info from user. Checks for
    validity. Creates a new instance of Account class and
    adds to db.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Redirects to home page route
    -------------------------------------------------------
    """
    if request.method == "POST":
        AccountTitle = request.form.get("accountTitle")
        UserName = request.form.get("userName")
        Email = request.form.get("email")
        Password = request.form.get("password")
        Additional = request.form.get("additional")

        if len(AccountTitle) < 1:
            flash("Account Title required")
        elif len(AccountTitle) > 60:
            flash("Account Title Too Long")
        elif len(UserName) > 60:
            flash("Username is too long")
        elif len(Password) > 60:
            flash("Password is too long")
        elif len(Email) > 60:
            flash("Email is too long")
        elif len(Additional) > 300:
            flash("Additional Info is too long")
        else:
            new_Account = Account(
                AccountTitle=cipher_suite.encrypt(AccountTitle.encode("utf-8")),
                UserName=cipher_suite.encrypt(UserName.encode("utf-8")),
                Email=cipher_suite.encrypt(Email.encode("utf-8")),
                Password=cipher_suite.encrypt(Password.encode("utf-8")),
                Additional=cipher_suite.encrypt(Additional.encode("utf-8")),
                user_id=current_user.id,
            )
            db.session.add(new_Account)
            db.session.commit()

    return redirect(url_for("views.home"))


@views.route("/delete-account", methods=["DELETE"])
def delete_account():
    """
    -------------------------------------------------------
    Handles POST requests for /delete-account endpoint.
    Retrieves accountId for account to be deleted. Queries
    db for account with matching id. Deletes account.
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        None
    -------------------------------------------------------
    """
    account = json.loads(request.data)
    account_id = account["accountId"]

    account = Account.query.get(account_id)
    if account:
        if account.user_id == current_user.id:
            db.session.delete(account)
            db.session.commit()

    return jsonify({})
