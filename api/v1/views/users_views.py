from flask import jsonify, request
from auth.auth import Authentication
from auth.user_auth import UserAuth
from datetime import datetime
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1/views/')

user_auth = UserAuth()
user_authenticator = Authentication()

@app_views.route('/register', methods=['POST'])
def register_user():
    """
    Register a new user
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')
    location = data.get('location')

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
    user_auth.create_user(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, location=location, is_superuser=is_superuser, is_active=is_active, last_login=last_login)
    return jsonify({"message": "user created successfully"}), 201

