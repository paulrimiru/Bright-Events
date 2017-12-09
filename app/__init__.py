"""
Code used to initialize the app module
"""
from flask import Flask
from instance.config import app_config
from .api import api
from .flasky import flasky

APP = Flask(__name__, instance_relative_config=True)

APP.config.from_object(app_config.get('config'))
APP.config.from_pyfile('config.py')

APP.register_blueprint(api, url_prefix='/api/v1')
APP.register_blueprint(flasky, url_prefix='/flasky')
