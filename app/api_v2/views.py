from datetime import datetime

from flask_restful import reqparse, fields, marshal_with, Resource
from app.api_v2 import API
from app.api_v1.utils.endpointparams import RegisterParams, LoginParams
from app.api_v2.models import User, DB, BCRYPT
from flask import current_app

from sqlalchemy.exc import IntegrityError
from flask_jwt import JWT, jwt_required, current_identity

def register_user(user_details):
    user = User(user_details['username'], user_details['email'], user_details['password'])
    DB.session.add(user)

    try:
        DB.session.commit()
    except IntegrityError:
        return {'success': False, 'message':'email already in exists in the system'}, 409  
    return {'id':user.id, 'username': user_details['username'], 'email':user_details['email']}, 201
def login_user(user_details):
    user = DB.session.query(User).filter(User.email == user_details['email']).first()
    if user and BCRYPT.check_password_hash(user.password, user_details['password']):
        return {'id':user.id, 'email': user_details['email']}, 200
    return {'success': True, 'message':'Invalid credentials'}
def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}

class RegisterUser(RegisterParams, Resource):
    def post(self):
        args = self.param.parse_args()
        return register_user(args)
class LoginUser(LoginParams, Resource):
    def post(self):
        args = self.param.parse_args()
        return login_user(args)
