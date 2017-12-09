from flask import Blueprint

flasky = Blueprint('flasky', __name__, 
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/flasky/static')

from . import views
