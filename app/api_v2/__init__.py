from flask import Blueprint
from flask_restful import Api
from flask import current_app
from flask_cors import CORS

api_v2 = Blueprint('api_v2', __name__)
CORS(api_v2)

API = Api(api_v2)

from app.api_v2.utils import routes
