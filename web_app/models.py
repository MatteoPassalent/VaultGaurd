from . import db

# Custom class
from flask_login import UserMixin

# references user.id from user class. User has multiple accounts (One to many relationship), foreign key must be in the child object
# Formatting: sql requires user to be lowercase
# id is the identifier between objects (primary key), doesnt need to be provided by user, will automatically be generated

# Account class is subclass of db.model
# Each class variable is a column (db.column). Data is stored in columns. Any class object that is initialized has to conform to data required below
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    AccountTitle = db.Column(db.String(200))
    UserName = db.Column(db.String(200))
    Email = db.Column(db.String(200))
    Password = db.Column(db.String(200))
    Additional = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# relationship is a column that stores account Id each time an account is created under each user object
# Inheriting from Usermixin allows use of methods that can be used for flask_login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))
    accounts = db.relationship("Account")
