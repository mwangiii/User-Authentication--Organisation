import pytest
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User, Organisation

@pytest.fixture
def app():
    """Create and configure a new Flask app instance for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)
        migrate = Migrate(app, db)
        jwt = JWTManager(app)
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client using the configured Flask app."""
    return app.test_client()

@pytest.fixture
def user_data():
    """Provide sample user data for testing."""
    return {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password',
        'phone': '1234567890'
    }

@pytest.fixture
def create_user(client, user_data):
    """Create a user in the database for testing."""
    user_data['password'] = generate_password_hash(user_data['password'])
    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    return user

def test_register_user(client, user_data):
    """Test user registration endpoint."""
    response = client.post('/auth/register', json=user_data)
    assert response.status_code == 201
    assert 'accessToken' in response.json['data']
    assert response.json['data']['user']['email'] == user_data['email']
    assert User.query.filter_by(email=user_data['email']).first()

def test_create_default_organisation_on_register(client, user_data):
    """Test creation of default organization on user registration."""
    response = client.post('/auth/register', json=user_data)
    assert response.status_code == 201
    assert Organisation.query.filter_by(name="John's Organisation").first()

def test_fail_login_with_invalid_data(client, create_user):
    """Test login with invalid credentials."""
    response = client.post('/auth/login', json={
        'email': 'john.doe@example.com',
        'password': 'not-password'
    })
    assert response.status_code == 401

def test_login_user_successfully(client, create_user):
    """Test successful user login."""
    response = client.post('/auth/login', json={
        'email': 'john.doe@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'accessToken' in response.json['data']
    assert response.json['data']['user']['email'] == 'john.doe@example.com'

def test_fail_registration_missing_fields(client):
    """Test registration failure due to missing required fields."""
    response = client.post('/auth/register', json={
        'firstName': 'John',
        'email': 'john.doe@example.com',
        'password': 'password',
        'phone': '1234567890'
    })
    assert response.status_code == 422
    assert response.json['errors'][0]['field'] == 'lastName'

def test_fail_registration_duplicate_email(client, create_user):
    """Test registration failure due to duplicate email."""
    response = client.post('/auth/register', json={
        'firstName': 'Jane',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password',
        'phone': '0987654321'
    })
    assert response.status_code == 422
    assert response.json['errors'][0]['field'] == 'email'

def test_generate_token_with_correct_user_details(client, create_user):
    """Test token generation with correct user details."""
    response = client.post('/auth/login', json={
        'email': 'john.doe@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    token = response.json['data']['accessToken']
    decoded_token = JWTManager().decode_token(token)
    assert decoded_token['sub'] == create_user.userId

def test_unauthorized_access_other_organisations(client, create_user):
    """Test unauthorized access to other organizations."""
    client.post('/auth/register', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password',
        'phone': '1234567890'
    })

    another_user = User(firstName='John', lastName='Another', email='john.another@example.com', password=generate_password_hash('password'))
    db.session.add(another_user)
    db.session.commit()

    organisation = User.query.filter_by(email='john.doe@example.com').first().organisations.first()

    with client.session_transaction() as session:
        session['user_id'] = another_user.id

    response = client.get('/api/organisations/' + organisation.orgId)
    assert response.status_code == 403

def test_authorize_access_own_organisations(client, create_user):
    """Test authorized access to own organizations."""
    organisation = Organisation(name="Test Organisation")
    create_user.organisations.append(organisation)
    db.session.commit()

    with client.session_transaction() as session:
        session['user_id'] = create_user.id

    response = client.get('/api/organisations/' + organisation.orgId)
    assert response.status_code == 200
