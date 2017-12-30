from flask_restful import reqparse, fields, marshal_with, Resource
from datetime import datetime
from app.api_v2 import API
from app.api_v1.utils.endpointparams import RegisterParams, LoginParams, EventParams, CategoryParams, PasswordResetParams
from app.api_v2.models import User, Event, Category,ResetPassword, DB, BCRYPT
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from sqlalchemy.exc import IntegrityError, InternalError

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
        return {'success':True, 'payload':{'access token':create_access_token({'id':user.id, 'email': user.email})}}, 200
    return {'success': True, 'message':'Invalid credentials'}, 401

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
class PasswordReset(PasswordResetParams, Resource):
    def post(self):
        args = self.param.parse_args()
        user = DB.session.query(User).filter(User.email == args['email']).first()
        if user:
            reset_pass = ResetPassword(user=user)
            DB.session.add(reset_pass)
            DB.session.commit()
            reset = DB.session.query(ResetPassword).filter(ResetPassword.user == user).first()
            return {'success':True, 'payload':{'code':reset.code}}, 201
        return {'success':False, 'message':'The user provided does not exist'}, 401
    def put(self):
        args = self.param.parse_args()
        reset = DB.session.query(ResetPassword).filter(ResetPassword.code == args['code']).filter(ResetPassword.date > datetime.now()).first()
        if reset:
            reset.user.encrypt_password(args['password'])
            DB.session.delete(reset)
            DB.session.commit()

            return {'success': True, 'payload':{'new password':args['password']}}, 200
        return {'success':False, 'message':'Code provided is either incorrect or expired'}, 401
class Events(EventParams, Resource):
    def post(self):
        args = self.param.parse_args()
        event = Event(args['name'], args['location'], args['host'], args['category'], args['time'])
        DB.session.add(event)

        try:
            DB.session.commit()
        except InternalError:
            return {'success':False, 'message': 'Could not proccess your request'}, 501

        return {'success': True, 'payload': args}, 201
class Categories(CategoryParams, Resource):
    def post(self):
        args = self.param.parse_args()
        category = Category(args['name'])
        DB.session.add(category)

        try:
            DB.session.commit()
        except InternalError:
            return {'success':False, 'message': 'Could not proccess your request'}, 501
        return {'success': True, 'payload': args}, 201
