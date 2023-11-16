from flask import Blueprint, jsonify, request, send_from_directory, url_for
from flask_jwt_extended import jwt_required
from models import db, User, UploadedFile
import os
from config import UPLOAD_FOLDER
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import uuid

upload_bp = Blueprint('upload', __name__)

# ONLY AUDIO, VIDEO FILES ALLOWED
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'wav'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """
    Uploads a file to the server and associates it with the logged-in user.

    Returns:
        A JSON response containing the message, filename, user_id, and file URL if the file is uploaded successfully.
        Otherwise, returns a JSON response with an error message.
    """
    current_user = get_jwt_identity()

    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    if file and allowed_file(file.filename):
        new_filename = secure_filename(file.filename)

        random_filename = str(uuid.uuid4()) + f".{file.filename.rsplit('.', 1)[1].lower()}"

        file.save(os.path.join(UPLOAD_FOLDER, random_filename))
        
        # Associate the uploaded file with the logged-in user
        user = User.query.filter_by(username=current_user).first()
        uploaded_file = UploadedFile(filename=new_filename, user_id=user.id, file=random_filename)
        db.session.add(uploaded_file)
        db.session.commit()

        return jsonify({"msg": "File uploaded successfully", "filename": uploaded_file.filename, "user_id": uploaded_file.user_id, "file": url_for('upload.download_file', filename=uploaded_file.file, _external=True)}), 201
    else:
        return jsonify({"msg": "File type not allowed"}), 400

@upload_bp.route('/files', methods=['GET'])
@jwt_required()
def get_files():
    """
    Returns a list of files uploaded by the authenticated user.

    Returns:
        A JSON object containing a list of files uploaded by the authenticated user.
        Each file object contains the filename, time created, download link, and user ID.
    """
    current_user = get_jwt_identity()

    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    uploaded_files = UploadedFile.query.filter_by(user_id=user.id).all()
    if not uploaded_files:
        return jsonify({"msg": "No files found for this user"}), 404

    files_data = []
    for file in uploaded_files:
        file_data = {
            "filename": file.filename,
            "time_created": file.time_created,
            "download_link": url_for('upload.download_file', filename=file.file, _external=True),
            "user_id": file.user_id,
        }
        files_data.append(file_data)

    return jsonify({"files": files_data}), 200


@upload_bp.route('/files/<filename>', methods=['GET'])
@jwt_required()
def download_file(filename):
    """
    Download a file from the server.

    Args:
        filename (str): The name of the file to be downloaded.

    Returns:
        The file to be downloaded with a 200 status code if the file exists.
        A JSON response with a 404 status code if the user or file is not found.
    """
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(username=current_user_id).first_or_404()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    user_file = UploadedFile.query.filter_by(user_id=user.id, file=filename).first()
    if not user_file:
        return jsonify({"msg": "File not found"}), 404
    
    return send_from_directory(UPLOAD_FOLDER, filename), 200
