"""
Code used to initialize the app module
""" 
from flask_api import FlaskAPI
from flask_restful import Api

APP = FlaskAPI(__name__, instance_relative_config=True)
API = Api(APP)
from app import routes

APP.config.from_object('config')
