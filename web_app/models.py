from . import db
from flask_login import UserMixin


# Note: id (in User) is the primary key, user_id (in Account) is foriegn key. One to many relationship


# Note: Account class is subclass of db.model
# Note: Each class variable is a column (db.column). Records stored in columns.
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AccountTitle = db.Column(db.String(200))
    UserName = db.Column(db.String(200))
    Email = db.Column(db.String(200))
    Password = db.Column(db.String(200))
    Additional = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# Note: Relationship is a column that stores the accountId of each account that is created by the user
# Note: Inherits from UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    accounts = db.relationship("Account")
