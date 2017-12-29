from flask import Blueprint
from flask_restful import Api

api_v1 = Blueprint('api_v1', __name__)

API = Api(api_v1)

from .utils import routes