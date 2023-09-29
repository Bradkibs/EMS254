#!/usr/bin/python3
"""
Flask App sends and accept json api requests to the set frontend
"""
from datetime import timedelta

from flask import Flask, jsonify, make_response, request
import os

# from flask_cors import CORS

from db import storage
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from auth.auth import Authentication
from api.v1.views.user import app_views
from api.v1.views.transactions import user_trans
from db.storage import DB

# from celery import Celery

db = DB()
db.reload()

Auth = Authentication()


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# broker_url = os.getenv('CELERY_BROKER_URL')
# celery = Celery(
#     app.import_name,
#     broker=broker_url
# )

#celery.conf.update(app.config, broker_connection_retry_on_startup=True)
# JWT config
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_COOKIE_SAMESITE'] = "None"





# Mail server config
# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
# app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')


app.url_map.strict_slashes = False

app.register_blueprint(app_views)
app.register_blueprint(user_trans)

host = os.getenv("APP_HOST", "0.0.0.0")
port = os.getenv("APP_PORT", 5000)
environ = os.getenv("APP_ENV")

if environ == 'development':
    app.debug = True
else:
    app.debug = False


# cors = CORS(app, origins="0.0.0.0")
# cors = CORS(app, resources={r'/*': {'origins': host}})
# cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# CORS(app_views, resources={r"/api/v1/views": {"origins": "http://localhost:5173"}},
#      supports_credentials=True)


@app.route("/")
def home():
    return jsonify({"Message": "Landing page display"}), 200
@app.route("/health")
def health():
    return jsonify({"Message": "Healthy!"}), 200

# @jwt.expired_token_loader
# def handle_expired_token_callback():
#     return redirect('/api/v1/views/login')


@app.before_request
def check_content_type():
    if request.method in ["POST", "PUT", "PATCH", "DELETE"] and request.headers["Content-Type"] != "application/json":
        return jsonify({"message": "Content-Type must be application/json"}), 400

@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_404(exception):
    """
    handles 400 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': str(err)}
        code = err.code
    else:
        message = {'error': str(err)}
        code = 500
    return make_response(jsonify(message), code)


@app.after_request
def add_cors_headers(response):
    frontend_url = "http://localhost:5173"
    response.headers.extend({
        'X-Content-Type-Options': 'no-sniff',
        'Access-Control-Allow-Origin': frontend_url,
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Headers': 'Content-Type, Cache-Control, X-Requested-With, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, DELETE'
    })


    return response



def setup_global_errors():
    """
    This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
