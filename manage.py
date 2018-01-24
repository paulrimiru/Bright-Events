"""Module handles the database migrations"""
import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import APP
from app.api_v2.models import DB
from instance.config import app_config

APP.config.from_object(app_config['production'])

migrate = Migrate(APP, DB)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    