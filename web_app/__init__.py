from flask import Flask

# Note: SQLALchemy is an Object Relational Mapper (ORM), allows easier interaction with database using a object oriented approach instead of raw SQL queiries
# Note: Using imbedded db, SQLite
from flask_sqlalchemy import SQLAlchemy

# Note: Path module contains methods related to file paths
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """
    -------------------------------------------------------
    Creates an instance of a Flask app. Configures app with
    SQLite db. Registers blueprints auth and views.
    Initializes and configures Login Manager
    Use: app = create_app()
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Initalized Flask application
    -------------------------------------------------------
    """
    # initliazes app
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = "matteo"
    # Sets URI: Database location and type (SQLite)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # Initializes and connects database with this flask app
    db.init_app(app)

    # imports view, auth blueprints and imports User class
    # Note: dot is relative import
    from .views import views
    from .auth import auth
    from .models import User

    # Registers blueprints with the main flask app
    app.register_blueprint(views)
    app.register_blueprint(auth)

    # Create a LoginManger instance
    login_manager = LoginManager()
    # Sets the login_view attribute to the login function in the auth blueprint. @login_required will redirect to auth.login function if user is not logged in
    login_manager.login_view = "auth.login"
    login_manager.login_message = None
    # Connects flask application
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        -------------------------------------------------------
        Defines the user loader callback function. Loads a user
        from the database when called by the login Manager. Used
        when current_user is accessed.
        Use: var = current_user
        -------------------------------------------------------
        Parameters:
            User id from user Class (defined in models)
        Returns:
            Instance of User class or None if not found
        -------------------------------------------------------
        """
        # Queries the database for a user object with a matching id
        return User.query.get(int(id))

    # Calls create_database
    create_database(app)

    return app


def create_database(app):
    """
    -------------------------------------------------------
    Creates a database if one does not already exist.
    Use: create_database(app)
    -------------------------------------------------------
    Parameters:
        app - a Flask application
    Returns:
        None
    -------------------------------------------------------
    """
    if not path.exists("VaultGuard_Password_Manager/" + DB_NAME):
        db.create_all(app=app)
