#!/usr/bin/python3
"""
Flask App sends and accept json api requests to the set frontend
"""
from datetime import timedelta

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS, cross_origin
import os
from db import storage
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # Set the token expiration time

app.url_map.strict_slashes = False

host = os.getenv("APP_HOST", "0.0.0.0")
port = os.getenv("APP_PORT", 5000)

cors = CORS(app, origins="0.0.0.0")
cors = CORS(app, resources={r'/*': {'origins': host}})
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.route("/")
def home():
    return jsonify("Hello world"), 200


@app.before_request
def check_content_type():
    if request.method in ["POST", "PUT", "PATCH"] and request.headers["Content-Type"] != "application/json":
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
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


@app.after_request
def add_cors_headers(response):
    response.headers.extend({
        'Access-Control-Allow-Origin': '*',
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
    app.run(host=host, port=port, debug=True)
