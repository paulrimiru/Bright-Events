from flask import Blueprint
from flask_restful import Api

api = Blueprint('api', __name__)

API = Api(api)

from .utils import routes