import os # Import os module
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'aliali110' # Old line
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key_for_dev') # Get from env or use default for dev
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from  .models import User, Note # Ensure models are imported so db.create_all() finds them
    
    create_database(app) # Call database creation
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Where to redirect if login is required
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Load user from database by ID
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all() # Create all defined database tables
            print("Database Created")