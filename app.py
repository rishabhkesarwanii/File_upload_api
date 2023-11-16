"""
The main application file for the Flask application.
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from routes.auth import auth_bp
from routes.upload import upload_bp
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(database_uri='sqlite:///database.sqlite'):
    """
    Creates and configures the Flask application.

    Args:
        database_uri (str): The URI for the database to use. Defaults to 'sqlite:///database.sqlite'.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)

    # Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    jwt = JWTManager(app)
    db.init_app(app)

    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.getenv('DEBUG'))
