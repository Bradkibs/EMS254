from flask import Blueprint

user_trans = Blueprint('user_trans', __name__, url_prefix='/api/v1/views/')


from api.v1.views.transactions.transact_view import *
