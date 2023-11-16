from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models import User
from models import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Registers a new user with the given username and password.

    Returns:
        A JSON response containing a success message, the username, and the user ID if the registration is successful.
        Otherwise, returns a JSON response containing an error message and a corresponding HTTP status code.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Signup successful", "username": new_user.username, "user_id": new_user.id}), 201  # Changed to 201 for resource created


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logs in a user with the provided username and password.
    
    Returns:
    - If successful, returns a JSON object containing the user's access token, id, and username with a status code of 200.
    - If unsuccessful, returns a JSON object with an error message and a status code of 400 or 401.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token, "id": user.id, "username": user.username}), 200

    return jsonify({"msg": "Invalid username or password"}), 401
