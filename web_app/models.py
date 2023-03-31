# . means from this package (website folder)
from . import db
# Custom class
from flask_login import UserMixin

# references data from user class, specifically column user.id. User has multiple notes (One to many relationship), must make the foreign key in the child object
# sql requires user to be lowercase, id is the field therefore user.id
#id is identifier between objects (primary key), doesnt need to be provided by user, will automatically be generated
class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    AccountTitle = db.Column(db.String(200))
    UserName = db.Column(db.String(200))
    Email = db.Column(db.String(200))
    Password = db.Column(db.String(200))
    Additional = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



#class is table where data is stored in columns. Whatever is put in the class has to conform to data required below
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))
    # relationship stores note Id each time note is created, uppercase required for sql
    accounts = db.relationship('Account')

