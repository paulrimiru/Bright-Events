"""
Code used to initialize the app module
"""
from flask import Flask

from instance.config import app_config
from .api_v1 import api_v1
from .api_v2 import api_v2
from .flasky import flasky
from .api_v2.models import DB, BCRYPT

from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

APP = Flask(__name__, instance_relative_config=True)

APP.config.from_object(app_config['development'])
APP.config.from_pyfile("config.py")

DB.init_app(APP)
BCRYPT.init_app(APP)

with APP.app_context():
    DB.create_all()

MIGRATE = Migrate(APP)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

APP.register_blueprint(api_v1, url_prefix='/api/v1')
APP.register_blueprint(api_v2, url_prefix='/api/v2')
APP.register_blueprint(flasky, url_prefix='/flasky')

swagger = Swagger(APP)
