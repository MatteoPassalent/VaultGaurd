from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Account
import json

# creates blueprint (mini flask app). Blueprint holds multiple routes inside
views = Blueprint("views", __name__)

# function below will run when the url with '/' prefix is accessed. ('views' blueprint replaces 'app')
# Handles http get request
@views.route("/", methods=["GET"])
# flask_login decorator that redirects user to auth.login function if not logged in. (set in init "login_manager.login_view = 'auth.login'")
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/", methods=["POST"])
@login_required
def add_account():
    # current user returns authenticated if logged in. Can use: user.is_aunthenticated in base.html
    if request.method == "POST":
        AccountTitle = request.form.get("accountTitle")
        UserName = request.form.get("userName")
        Email = request.form.get("email")
        Password = request.form.get("password")
        Additional = request.form.get("additional")

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

    return redirect(url_for("views.home"))


@views.route("/delete-account", methods=["POST"])
def delete_account():
    account = json.loads(request.data)
    account_id = account["accountId"]
    account = Account.query.get(account_id)
    if account:
        if account.user_id == current_user.id:
            db.session.delete(account)
            db.session.commit()

    return jsonify({})
