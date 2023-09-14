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
    is_active = False
    is_superuser = False
    last_login = datetime.utcnow()
    last_login_str = last_login.strftime("%Y-%m-%d %H:%M:%S")
    user = user_auth.get_user_by_email(email)
    # user_data = {
    #     "email": user.email,
    #     "password": user.password,
    #     "first_name": user.first_name,
    # }

    # return jsonify(user_data), 200
    if user:
        return jsonify({"message": "user already exists"}), 409
    else:
        usr = user_auth.create_user(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, location=location, is_superuser=is_superuser, is_active=is_active, last_login=last_login_str)
        return jsonify({"message": "user created successfully", "user_id": str(usr.id) }), 201


@app_views.route('/login', methods=['POST'])
def login_user():
    """
    Login a user
    """
    data = request.get_json()
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not email and not phone_number:
        return jsonify({"message": "email or phone number is required"}), 400
    if not password:
        return jsonify({"message": "password is required"}), 400
    if email:
        user = user_auth.get_user_by_email(email)
        if not user:
            return jsonify({"message": "user not found"}), 404
        if not user_auth.verify_password(password, user.password):
            return jsonify({"message": "invalid password"}), 400
        else:
            access_token = user_authenticator.create_token(user.id)
            response = jsonify({"message":"Logged in successfully!", 'status': 200})
            user_authenticator.set_cookie(response, access_token)
            return response
    if phone_number:
        user = user_auth.get_user_by_email(phone_number)
        if not user:
            return jsonify({"message": "user not found"}), 404
        if not user_auth.verify_password(password, user.password):
            return jsonify({"message": "invalid password"}), 400
        else:
            access_token = user_authenticator.create_token(user.id)
            response = jsonify({"message":"Logged in successfully!", 'status': 200})
            user_authenticator.set_cookie(response, access_token)
            return response


# @app_views.route('/users/<string:user_id>', methods=['GET'])
# def get_user(user_id):
#     """
#     Get a user
#     """
#     user = user_auth.get_user_by_id(user_id)
#     if not user:
#         return jsonify({"message": "user not found"}), 404
#     user_data = {
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "phone_number": user.phone_number,
#         "location": user.location,
#         "is_superuser": user.is_superuser,
#         "is_active": user.is_active,
#         "last_login": user.last_login

#     }
#     return jsonify(user_data), 200
