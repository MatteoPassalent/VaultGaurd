from . import db
from flask_login import UserMixin

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AccountTitle = db.Column(db.String(200))
    UserName = db.Column(db.String(200))
    Email = db.Column(db.String(200))
    Password = db.Column(db.String(200))
    Additional = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    accounts = db.relationship("Account")
