"""
Database models for the application.
"""
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    """
    A class representing a user in the system.

    Attributes:
    -----------
    id : int
        The unique identifier for the user.
    username : str
        The username of the user.
    password_hash : str
        The hashed password of the user.
    is_active : bool
        A flag indicating whether the user is active or not.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class UploadedFile(db.Model):
    """
    Represents a file uploaded by a user.

    Attributes:
        id (int): The unique identifier for the uploaded file.
        filename (str): The name of the uploaded file.
        file (str): The path to the uploaded file.
        user_id (int): The ID of the user who uploaded the file.
        time_created (datetime): The date and time the file was uploaded.
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    time_created = db.Column(db.DateTime, server_default=db.func.now())