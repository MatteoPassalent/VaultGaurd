from flask import Flask

# COME BACK LATER AND DO PROPER FUNCTION DESCRIPTIONS FOR REVIEW
# SQLALchemy is an Object Relational Mapper (ORM), allows easier interaction with database using a object oriented approach instead of raw SQL queiries
from flask_sqlalchemy import SQLAlchemy

# from operating system import path module which contains functions related to file paths
from os import path
from flask_login import LoginManager

# initializes and defines database name, DB_NAME is property and rs is chosen name
db = SQLAlchemy()
DB_NAME = "database.db"

# create_app function, app = flask(__name__) initliazes app.
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "matteo"
    # database is located at that location
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # Initializes and connects database with this flask app
    db.init_app(app)

    # dot is reletive import, it means its from the same website folder
    # imports view, auth blueprints and imports User class
    from .views import views
    from .auth import auth
    from .models import User

    # Registers previously imported blueprints with the main flask app
    app.register_blueprint(views)
    app.register_blueprint(auth)

    # initializes login manager
    # Create a LoginManger instance
    login_manager = LoginManager()
    # Sets the login_view attribute to the login function in the auth blueprint. @login_required will redirect to auth.login function if user is not logged in
    login_manager.login_view = "auth.login"
    # Msg defaults to true, force none
    login_manager.login_message = None
    # Connects flask application
    login_manager.init_app(app)

    # tells flask how to load a user, query looks for primary key. Returns id or none if user doesnt exist. Is not called directly but instead through internal loginmanager functions
    # The decorator registers the function as the "user loader callback function". Which loads a user object from the database
    @login_manager.user_loader
    # id is the unique user id defined in the User class in the models module
    def load_user(id):
        # queries the database for a user object with a matching id
        return User.query.get(int(id))

    # Calls create_database function below
    create_database(app)

    return app


# creates database only if it doesnt already exist
def create_database(app):
    if not path.exists("VaultGuard_Password_Manager/" + DB_NAME):
        db.create_all(app=app)
