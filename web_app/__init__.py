from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from operating system import path
from os import path
from flask_login import LoginManager

# initializes and defines database name, DB_NAME is property and rs is chosen name
db = SQLAlchemy()
DB_NAME = "database.db"

# create_app function, app = flask(__name__) initliazes app, secret_key is a secret key. Why does this function run?


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'matteo'
    # database is located at that location
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app will be used for db database
    db.init_app(app)

    # dot is reletive import, it means its from the same website folder
    from .views import views
    from .auth import auth
    from .models import User

    # prefix is what is placed before url in route brackets, dont want anything here
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    # initializes login manager

    # Create a LoginManger instance
    login_manager = LoginManager()

    # Define the scope
    login_manager.login_view = 'auth.login'

    # Msg defaults to true, force none
    login_manager.login_message = None

    # Connect application
    login_manager.init_app(app)

    # tells flask how to load a user, query default looks for primary key. Returns id
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# creates database only if it doesnt already exist


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
