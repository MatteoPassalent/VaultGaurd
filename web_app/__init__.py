from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from os import path
from flask_login import LoginManager
from cryptography.fernet import Fernet

db = SQLAlchemy()
DB_NAME = "database.db"

# Needs to be stored securely for launching
if path.exists("web_app\config.txt"):
    with open("web_app\config.txt", "rb") as file:
        secret_key = file.readline()
        file.close()
else:
    with open("web_app\config.txt", "wb") as file:
        secret_key = Fernet.generate_key()
        file.write(secret_key)
        file.close()

cipher_suite = Fernet(secret_key)


def create_app():
    """
    -------------------------------------------------------
    Creates an instance of a Flask app. Configures app with
    SQLite db. Registers blueprints auth and views.
    Initializes and configures Login Manager
    -------------------------------------------------------
    Parameters:
        None
    Returns:
        Initalized Flask application
    -------------------------------------------------------
    """
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = "matteo"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views)
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = None
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        -------------------------------------------------------
        Defines the user loader callback function. Loads a user
        from the database when called by the login Manager. Used
        when current_user is accessed.
        -------------------------------------------------------
        Parameters:
            User id from user Class (defined in models)
        Returns:
            Instance of User class or None if not found
        -------------------------------------------------------
        """
        return User.query.get(int(id))

    @app.template_filter("decrypt")
    def decrypt_and_decode_filter(value):
        decrypted_value = cipher_suite.decrypt(value).decode("utf-8")
        return decrypted_value

    create_database(app)

    return app


def create_database(app):
    """
    -------------------------------------------------------
    Creates a database if one does not already exist.
    -------------------------------------------------------
    Parameters:
        app - a Flask application
    Returns:
        None
    -------------------------------------------------------
    """
    if not path.exists("VaultGuard_Password_Manager/" + DB_NAME):
        db.create_all(app=app)
