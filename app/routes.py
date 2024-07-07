from flask import Flask, jsonify, request
from app import app,db
import jwt
from app.models import User
from app.models import Organisation
from app.models import UserOrganisation
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os


@app.route("/")
def home_page():
    return "Welcome!"

@app.route("/auth")
def auth_page():
    return "<div></div>"

@app.route("/api")
def api_page():
    return "<div></div>"

# Function to add errors to a list
def add_error_to_list(errors_list, field, message):
    errors_list.append({
        "field": field,
        "message": message
    })
# using jwt to generate token
def generate_jwt_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1), 
            'iat': datetime.utcnow(), 
            'sub': str(userid)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        return jwt_token
    except Exception as e:
        return str(e)

# Registers a user and creates a default organisation
@app.route("/auth/register", methods=['POST'])
def register_user():
    data = request.json
    errors_list = []

    # Validating required fields
    if not data.get('firstName'):
        add_error_to_list(errors_list, field="firstName", message="First name is required")
    if not data.get('lastName'):
        add_error_to_list(errors_list, field="lastName", message="Last name is required")
    if not data.get('email'):
        add_error_to_list(errors_list, field="email", message="Email is required")
    if not data.get('password'):
        add_error_to_list(errors_list, field="password", message="Password is required")

    # Check if email is already registered
    if User.query.filter_by(email=data['email']).first():
        add_error_to_list(errors_list, field="email", message="Email Address already in use")

    # If there are validation errors, return 400 status code with errors
    if errors_list:
        return jsonify({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "errors": errors_list
        }), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(data['password'], method='sha256')

    # Create a new user object
    new_user = User(
        firstname=data['firstName'],
        lastname=data['lastName'],
        email=data['email'],
        password=hashed_password,
        phone=data.get('phone')
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        # Generate JWT token for the new user
        jwt_token = generate_jwt_token(new_user.userid)

        # Return successful response with JWT token and user data
        return jsonify({
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": jwt_token.decode('utf-8'),
                "user": {
                    "userId": str(new_user.userid),
                    "firstName": new_user.firstname,
                    "lastName": new_user.lastname,
                    "email": new_user.email,
                    "phone": new_user.phone
                }
            }
        }), 201 
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Registration unsuccessful",
            "error": str(e)
        }), 500


# Logs in a user. When you log in, you can select an organisation to interact with
@app.route("/auth/login", methods=['POST'])
def login_user():
    data = request.json
    existing_user = {
        "email": data['email'],
        "password": data['password']
    }
    response_successful = {
        "status": "success",
        "message": "Login successful",
        "data": {
            "accessToken": "eyJh...",
            "user": {
                "userId": "string",
                "firstName": "string",
                "lastName": "string",
                "email": "string",
                "phone": "string"
            }
        }
    }

    response_unsuccessful = {
        "status": "Bad request",
        "message": "Authentication failed",
        "statusCode": 401
    }
    try:
        db.session.query(existing_user)
        db.session.commit()
        return jsonify(response_successful)
    except Exception as e:
        db.session.rollback()
        return jsonify(response_unsuccessful)

# A user gets their own record or user record in organisations they belong to or created [PROTECTED]
@app.route("/api/users/<id>", methods=['GET'])
def get_users_by_id(id):
    response_successful = {
        "status": "success",
        "message": "<message>",
        "data": {
            "userId": id,
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "phone": "string"
        }
    }
    try:
        db.session.query(id)
        db.session.commit()
        return jsonify(response_successful)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Gets all the organisations the user belongs to or created [PROTECTED]
@app.route("/api/organisations", methods=['GET'])
def get_organizations():
    response_successful = {
        "status": "success",
        "message": "<message>",
        "data": {
            "organisations": [
                {
                    "orgId": "string",
                    "name": "string",
                    "description": "string",
                }
            ]
        }
    }
    try:
        db.session.query(Organisation)
        db.session.commit()
        return jsonify(response_successful)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# The logged-in user gets a single organisation record [PROTECTED]
@app.route("/api/organisations/<orgId>", methods=['GET'])
def get_organization_by_id(orgId):
    response_successful = {
        "status": "success",
        "message": "<message>",
        "data": {
            "orgId": orgId,
            "name": "string",
            "description": "string",
        }
    }
    try:
        db.session.query(orgId)
        db.session.commit()
        return jsonify(response_successful)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# A user can create their new organisation [PROTECTED]
@app.route("/api/organisations", methods=['POST'])
def create_organization():
    data = request.json
    create_organisation = {
        "orgid": "string",
        "name": data['name'],
        "description": data['description']
    }
    return "helloworld"

# Adds a user to a particular organisation
@app.route("/api/organisations/<orgId>/users", methods=['POST'])
def add_user_to_organization(orgId):
    data = request.json
    new_organisation = {
        "userid": "string",
        "orgid": orgId
    }
    try:
        db.session.add(new_organisation)
        db.session.commit()
        return jsonify({"message": "User added to organization"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
