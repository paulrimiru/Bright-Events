"""
Module contains all the routes required by the API
"""

from app.api_v2 import API as restful
from app.api_v2 import views as funcs

restful.add_resource(funcs.RegisterUser, '/auth/register')
restful.add_resource(funcs.LoginUser, '/auth/login')
restful.add_resource(funcs.Events, '/events')
restful.add_resource(funcs.Categories, '/categories')
restful.add_resource(funcs.PasswordReset, '/auth/reset-password')
