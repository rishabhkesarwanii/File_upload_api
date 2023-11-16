"""
This module contains the tests for the application.
"""
import pytest
from app import create_app
from models import db
import os


@pytest.fixture(scope='module')
def test_client():        
    """
    Function to create a test client for the Flask application.

    Returns:
    testing_client: Flask test client instance
    """
    app = create_app(database_uri='sqlite:///:memory:')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client  

            # Clean up after testing
            db.drop_all()

def test_signup(test_client):
    """
    Test the signup functionality of the application.
    """
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/signup', json=payload)
    assert response.status_code == 201

def test_login(test_client):
    """
    Test the login functionality of the application.
    """
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/login', json=payload)
    assert response.status_code == 200 
    assert 'access_token' in response.json 

def test_login_wrong_password(test_client):
    """
    Test the login functionality of the application with a wrong password.
    """
    payload = {
        "username": "testuser",
        "password": "testpasswor"
    }
    response = test_client.post('/login', json=payload)
    assert response.status_code == 401 
    assert 'access_token' not in response.json 

def test_login_wrong_username(test_client):
    """
    Test the login functionality of the application with a wrong username.
    """
    payload = {
        "username": "testus",
        "password": "testpassword"
    }
    response = test_client.post('/login', json=payload)
    assert response.status_code == 401 
    assert 'access_token' not in response.json 

def test_file_upload(test_client):
    """
    Test the file upload functionality of the application.
    """
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/login', json=payload)
    access_token = response.json['access_token']

    with open(os.path.join("testfiles", "test.mp3"), 'rb') as f:
        response = test_client.post('/upload', data={'file': f}, headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 201 
        assert 'filename' in response.json 
        assert 'user_id' in response.json 
        assert 'file' in response.json


def test_file_upload_no_file(test_client):
    """
    Test the file upload functionality of the application with no file.
    """
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/login', json=payload)
    access_token = response.json['access_token']

    response = test_client.post('/upload', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 400

def test_file_upload_wrong_file_type(test_client):
    """
    Test the file upload functionality of the application with a file type that is not allowed.
    """
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/login', json=payload)
    access_token = response.json['access_token']

    with open(os.path.join("testfiles", "test.txt"), 'rb') as f:
        response = test_client.post('/upload', data={'file': f}, headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 400


def test_get_files(test_client):
    """
    Test the get files functionality of the application.
    """
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/login', json=payload)
    access_token = response.json['access_token']

    response = test_client.get('/files', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200 
    assert 'files' in response.json


def test_get_files_no_files(test_client):
    """
    Test the get files functionality of the application with no files.
    """
    payload = {
        "username": "testuser2",
        "password": "testpassword2"
    }
    response = test_client.post('/signup', json=payload)
    assert response.status_code == 201 

    payload = {
        "username": "testuser2",
        "password": "testpassword2"
    }
    response = test_client.post('/login', json=payload)
    access_token = response.json['access_token']

    response = test_client.get('/files', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 404


def test_download_file(test_client):
    """
    Test the download file functionality of the application.
    """
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/login', json=payload)
    access_token = response.json['access_token']

    response = test_client.get('/files', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200 
    assert 'files' in response.json
    filename = response.json['files'][0]['download_link'].split('/')[-1]
    response = test_client.get(f'/files/{filename}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.content_type == 'audio/mpeg'
    