from app import app_views
from flask import jsonify, abort, request
from auth.auth import Authentication
from auth.user import UserAuth
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

user_auth = UserAuth()
user_authenticator = Authentication()

@app_views.route('/register', methods=['POST'])
def register_user():
    """
    Register a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone_number = request.form.get('phone_number')
    location = request.form.get('location')

    if not email:
        return jsonify({"message": "email is required"}), 400
    if not password:
        return jsonify({"message": "password is required"}), 400
    if not first_name:
        return jsonify({"message": "first_name is required"}), 400
    if not last_name:
        return jsonify({"message": "last_name is required"}), 400
    if not phone_number:
        return jsonify({"message": "phone_number is required"}), 400
    if not location:
        return jsonify({"message": "location is required"}), 400
    is_active = True
    is_superuser = False
    last_login = datetime.utcnow()
    user = user_auth.create_user(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, location=location, is_superuser=is_superuser, is_active=is_active, last_login=last_login)
    return jsonify({"message": "user created successfully"}), 201

@app_views.route('/users', methods=['GET'], strict_slashes=False)
