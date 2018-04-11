from datetime import datetime
from flask import url_for, jsonify
from flask_restful import Resource
from app.api_v2 import API
from instance.config import app_config

from app.api_v1.utils.endpointparams import RegisterParams, LoginParams, \
                                            EventParams, \
                                            PasswordResetParams, RsvpParams, \
                                            SearchParam 
from app.api_v2.models import Users, Event, Rsvp, ResetPassword, DB, \
                              BCRYPT, events_schema, rsvp_schema, rsvps_schema, TokenBlackList, \
                              JWTMANAGER, event_schema, MAIL
from flask_jwt_extended import jwt_required, create_access_token, \
                                get_raw_jwt

from sqlalchemy.exc import IntegrityError, InternalError
from flask_mail import Message
from instance.config import Config
import json
import datetime
import re

@JWTMANAGER.expired_token_loader
def token_expiry_response():
    return jsonify({
        'status': False,
        'message': 'token provided is expired please login again'
    })

def validate_email(email):
    """validates if the email provided is the correct email"""
    regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if regex.match(email):
        return True
    return False
def validate_password(password):
    """chaecks for password strength"""
    repetitve_reg =  re.compile(r'(\w)\1*')
    length_reg = re.compile(r'.{6,}')
    uppercase_reg = re.compile(r'[A-Z]')
    lowercase_reg = re.compile(r'[a-z]')
    digit_reg = re.compile(r'[0-9]')
    special_reg = re.compile(r'[!@#$%&*]')

    if length_reg.search(password):
        if uppercase_reg.search(password):
            if lowercase_reg.search(password):
                if digit_reg.search(password):
                    if special_reg.search(password):
                        if repetitve_reg.search(password):
                            return {'success':True}
                        return {'success':False, 'message':'password must not  contain repetitive letters characters'}
                    return {'success':False, 'message':'password must contain special characters'}
                return {'success':False, 'message':'password must contain sa digit'}
            return {'success':False, 'message':'password must contain lower case characters'}
        return {'success':False, 'message':'password must contain upper case characters'}
    return {'success':False, 'message':'password must be six characters or longer'}
def validate_params(params):
    """validates thet params passed are not empty"""
    for param in params:
        if isinstance(params.get(param), str) and params.get(param) == "":
            return False
    return True
def register_user(user_details):
    """Registers users"""
    print(user_details)
    if user_details['email'] and user_details['password'] and user_details['username']:
        passwor_val = validate_password(user_details['password'])

        if passwor_val.get('success'):
            if validate_password(user_details['password']):
                user = Users(user_details['username'], user_details['email'], user_details['password'])
                DB.session.add(user)
                try:
                    DB.session.commit()
                except IntegrityError:
                    return {'success': False, 'message':'email already in exists in the system'}, 406  
                return {'id':user.id, 'username': user_details['username'], 'email':user_details['email']}, 201
            return {'success': False, 'message':'Please provide a password of more than 6 characters long'}, 406 
        return {'success': False, 'message':passwor_val.get('message')}, 406
    return {'success':False, 'message':'please ensure that all your details are provided'}, 406

def login_user(user_details):
    """handles user login"""
    if user_details['email'] and user_details['password']:
        if validate_email(user_details['email']):
            user = DB.session.query(Users).filter(Users.email == user_details['email']).first()
            if user and BCRYPT.check_password_hash(user.password, user_details['password']):
                return {'success':True, 'payload':{'user_id':user.id, 'token':create_access_token({'id':user.id, 'email': user.email}, expires_delta=datetime.timedelta(days=1))}}, 200
            return {'success': False, 'message':'Invalid credentials'}, 401
        return {'success': False, 'message':'please provide a valid email'}, 409 
    return {'success':True, 'message':'please ensure that you provide all your details'}, 409

def isStringBool(sample):
    """checks if a String provided is a boolean"""
    if sample in ("True", "False", "true", "false"):
        return True
    return False

def identity(payload):
    """extracts the identity of a token"""
    user_id = payload['identity']
    return {"user_id": user_id}

@JWTMANAGER.token_in_blacklist_loader
def check_if_token_is_blacklisted(token):
    """checks if a token ha been black listed"""
    jwt_token = token.get('jti')
    mytoken = DB.session.query(TokenBlackList).filter(TokenBlackList.token == jwt_token).first()
    if mytoken:
        return True
    return False
class RegisterUser(RegisterParams, Resource):
    """resource to perform user registration"""
    def post(self):
        """
        Register users
        ---
        tags:
            - Registration V2
        parameters:
            - in: formData
              name: username
              type: string
              required: true
            - in: formData
              name: email
              type: string
              required: true
            - in: formData
              name: password
              type: string
              required: true
        responses:
            201:
                description: A single user item
            406:
                description: Another user with the same email is found
        """
        args = self.param.parse_args()
        return register_user(args)
class LoginUser(LoginParams, Resource):
    """resource to perform user login"""
    def post(self):
        """
        Login users
        ---
        tags:
            - Authentication V2
        parameters:
            - in: formData
              name: email
              type: string
              required: true
            - in: formData
              name: password
              type: string
              required: true
        responses:
            201:
                description: Authenticated user
            401:
                description: User credentials are wrong
        """
        args = self.param.parse_args()
        return login_user(args)
class LogoutUser(Resource):
    """resource to perform user logout functionality"""
    @jwt_required
    def post(self):
        """
        Logout users
        ---
        tags:
            - Authentication V2
        parameters:
            - in: formData
              name: id
              type: string
              required: true
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: true
        responses:
            201:
                description: User logged out
            401:
                description: User already logged out
        """
        token = get_raw_jwt()
        tokenblacklist = TokenBlackList(token.get('jti'), token.get('identity').get('id'), datetime.datetime.fromtimestamp(token.get('exp')))
        DB.session.add(tokenblacklist)
        DB.session.commit()
        return {'success':True, 'payload':{'user_id':token.get('identity').get('id')}}
        
class PasswordReset(PasswordResetParams, Resource):
    """resource to perform user password reset functionality"""
    def post(self):
        """
        Reset users password
        ---
        tags:
            - Authentication V2
        parameters:
            - in: formData
              name: email
              type: string
              required: true
        responses:
            201:
                description: Reset code sent to user
            401:
                description: Email provided does not exist
        """
        args = self.param.parse_args()
        user = DB.session.query(Users).filter(Users.email == args['email']).first()
        if user:
            reset_pass = ResetPassword(user=user)
            DB.session.add(reset_pass)
            DB.session.commit()
            reset = DB.session.query(ResetPassword).filter(ResetPassword.user == user).first()
            
            msg = Message("Verification code", sender=Config.ADMINS[0], recipients=[args['email']])
            msg.body = "Hey there here is your verification code: " + reset.code
            MAIL.send(msg)

            return {'success':True, 'message':'code was sent to your mail'}, 201
        return {'success':False, 'message':'The user provided does not exist'}, 401
    def put(self):
        """
        Reset password using confimation code sent
        ---
        tags:
            - Authentication V2
        parameters:
            - in: formData
              name: code
              type: string
              required: true
            - in: formData
              name: password
              type: string
              required: true
        responses:
            200:
                description: Password reset succesfully
            401:
                description: Code provided is not valid
        """
        args = self.param.parse_args()
        reset = DB.session.query(ResetPassword).filter(ResetPassword.code == args['code']).filter(ResetPassword.date > datetime.datetime.now()).first()
        if reset:
            reset.user.encrypt_password(args['password'])
            DB.session.delete(reset)
            DB.session.commit()

            return {'success': True, 'payload':{'new password':args['password']}}, 200
        return {'success':False, 'message':'Code provided is either incorrect or expired'}, 401
def encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
class Events(EventParams, Resource):
    """resource to perform event creation and retrieval"""
    def get(self):
        """
        Retreive all events
        ---
        tags:
            - Events V2
        parameters:
            - in: query
              name: page
              type: int
              required: false
        responses:
            201:
                description: Events retrieved
            401:
                description: Events could not be retrieved
        """
        args = self.param.parse_args()
        page = args.get('page', 1)
        limit = args.get('limit', app_config['limit'])
        events = Event.query.paginate(page, limit, False)
        myresult = events_schema.dump(events.items)
        if bool(myresult.data):
            next_url=""
            previous_url=""
            if events.has_next:
                next_url = API.url_for(Events, limit=args.get('limit'), page=events.next_num)
            if events.has_prev:
                previous_url = API.url_for(Events, limit=args.get('limit'), page=events.prev_num)
            return {'success':True,'page_navigation':{'next':next_url, 'previous':previous_url} ,'payload':{'event_list':myresult.data}}, 200
        return {'success':False, 'message':'sorry no events at the momment'}, 401

    @jwt_required
    def post(self):
        """
        Create event
        ---
        tags:
            - Events V2
        parameters:
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: true
            - in: formData
              name: name
              type: string
              required: true
            - in: formData
              name: location
              type: string
              required: true
            - in: formData
              name: category
              type: string
              required: true
            - in: formData
              name: time
              type: string
              required: true
            - in: formData
              name: host
              type: int
              required: true
            - in: formData
              name: private
              type: boolean
              required: true
        responses:
            201:
                description: Event created successfully
            401:
                description: Event not created
        """

        args = self.param.parse_args()
        if args['host'] and isinstance(args['host'], int):
            if validate_params(args):
                event = Event(args['name'], args['location'], args['host'], args['category'], args['time'])
                DB.session.add(event)
                try:
                    DB.session.commit()
                except IntegrityError :
                    return {'success':False, 'message': 'Could not proccess your request'}, 401
                DB.session.refresh(event)
                args.update({'id':str(event.id)})
                return {'success': True, 'payload': {'event_id':str(event.id)}}, 201
            return {'success':False, 'message':'please ensure that all the details are correct'}, 401
        return {'success':False, 'message':'Please ensure that the host field is not empty and is an integer'}, 401
    
class ManageEvents(EventParams, Resource):
    """Resource to perfrm event editing, single event retrieval and deletion"""
    def get(self, event_id):
        """
        get single event
        ---
        tags:
            - Events V2
        parameters:
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: true
            - in: path
              name: event_id
              type: string
              required: true
        responses:
            201:
                description: Specific event edited successfully
            401:
                description: Event could not be edited
        """
        if isinstance(event_id, int)or isinstance(int(event_id), int):
            event = Event.query.get(event_id)
            if event:
                result = event_schema.dump(event)
                return {'success':True, 'payload':result.data}, 200
            return {'success':False, 'message':'sorry could not find the requested event'}, 401
        return {'success':False, 'message': 'invalid event id'}, 401

    @jwt_required
    def put(self, event_id):
        """
        Edit specific Event
        ---
        tags:
            - Events V2
        parameters:
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: false
            - in: path
              name: event_id
              type: string
              required: true
            - in: formData
              name: name
              type: string
              required: false
            - in: formData
              name: location
              type: string
              required: false
            - in: formData
              name: category
              type: string
              required: false
            - in: formData
              name: time
              type: string
              required: false
        responses:
            201:
                description: Specific event edited successfully
            401:
                description: Event could not be edited
        """
        if isinstance(event_id, int) or isinstance(int(event_id), int):
            event = DB.session.query(Event).get(event_id)
            args = self.param.parse_args()
            if event:
                if args['name']:
                    event.name = args['name']
                if args['location']:
                    event.location = args['location']
                if args['category']:
                    event.category = args['category']
                if args['time']:
                    event.time = args['time']
                
                DB.session.commit()
                DB.session.refresh(event)
                return {'success':True, 'payload':event_schema.dump(event)[0]}, 200
            return {'success':False, 'message':'event not found'}, 401
        return{'success':False, 'message':'invalid  event id'}
    @jwt_required
    def delete(self, event_id):
        """
        Delete specific Event
        ---
        tags:
            - Events V2
        parameters:
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: true
            - in: path
              name: event_id
              type: string
              required: true
        responses:
            201:
                description: Event deleted successfully
            401:
                description: Event could not be deleted
        """
        if isinstance(event_id, int)or isinstance(int(event_id), int):
            event = Event.query.get(event_id)
            rsvpslist = Rsvp.query.filter_by(event_id = event_id).all()
            if bool(rsvpslist):
                for rsvp in rsvpslist:
                    DB.session.delete(rsvp)
                DB.session.commit()
            if event:
                DB.session.delete(event)
                DB.session.commit()
                return {'success': True, 'payload':{'id':event_id}}, 200
            return {'success':False, 'message':'event not found'}, 401
        return {'success':False, 'message':'invalid event id'}, 401

class SearchEvent(SearchParam, Resource):
    """resource to carry out event searching"""
    @jwt_required
    def get(self):
        """
        Retreive all events
        ---
        tags:
            - Events V2
        parameters:
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: true
            - in: query
              name: q
              type: string
              description: search event by name
              required: true
            - in: query
              name: location
              type: string
              description: filter events by location
              required: false
            - in: query
              name: category
              type: string
              description: filter events by category
              required: false
        responses:
            201:
                description: Events retrieved
            401:
                description: Events could not be retrieved
        """
        args = self.param.parse_args()
        myresult = None
        events = None
        if args["q"]:
            if args["location"]:
                if args["category"]:
                    events = DB.session.query(Event).filter(Event.name.like(args['q'])).filter(Event.location == args["location"]).filter(Event.category == args["category"])
                    myresult = events_schema.dump(events)
                    if bool(myresult.data):
                        return {'success':True, 'payload':{'event_list':myresult.data}}, 200
                    return {'success':False, 'message':'sorry no events in this location in that category'}, 401
                events = DB.session.query(Event).filter(Event.name.like(args['q'])).filter(Event.location == args["location"])
                myresult = events_schema.dump(events)
                if bool(myresult.data):
                    return {'success':True, 'payload':{'event_list':myresult.data}}, 200
                return {'success':False, 'message':'sorry no events in this location'}, 401
            elif args["category"]:
                events = DB.session.query(Event).filter(Event.name.like(args['q'])).filter(Event.category == args["category"])
                myresult = events_schema.dump(events)
                if bool(myresult.data):
                    return {'success':True, 'payload':{'event_list':myresult.data}}, 200
                return {'success':False, 'message':'sorry no events in this category'}, 401
            events = DB.session.query(Event).filter(Event.name.like(args['q']))
            myresult = events_schema.dump(events)
            if bool(myresult.data):
                return {'success':True, 'payload':{'event_list':myresult.data}}, 200
            return {'success':False, 'message':'sorry no events in this name'}, 401
        return {'success':False, 'message':'please ensure you pass a name to search'}, 401
class ManageRsvp(RsvpParams, Resource):
    """event to carry out rsvp CRUD operation"""
    @jwt_required
    def get(self, event_id):
        """
        Retrieve Rsvp for a particular event
        ---
        tags:
            - Rsvp V2
        parameters:
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: true
            - in: query
              name: page
              type: int
              required: false
            - in: path
              name: event_id
              type: string
              required: true
        responses:
            201:
                description: Rsvp retrived successfully
            401:
                description: Rsvp not added to event
        """
        args = self.param.parse_args()
        page = args.get('page', 1)
        limit = args.get('limit', app_config['limit'])
        rsvp = DB.session.query(Rsvp).filter(Rsvp.event_id == event_id).paginate(page, limit, False)
        data = rsvps_schema.dump(rsvp.items).data
        if data:
            next_url=""
            previous_url=""
            if rsvp.has_next:
                next_url = API.url_for(ManageRsvp, event_id=event_id,page=rsvp.next_num)
            if rsvp.has_prev:
                previous_url = API.url_for(ManageRsvp, event_id=event_id,page=rsvp.prev_num)
            return {'success':True, 'page_navigation':{'next':next_url, 'previous':previous_url}, 'payload':data}, 200
        return {'success':False, 'message':'there are no rsvps for that event'}, 401

    def post(self, event_id):
        """
        Rsvp a particular event
        ---
        tags:
            - Events V2
        parameters:
            - in: path
              name: event_id
              type: int
              required: true
            - in: formData
              name: client_email
              type: string
              required: true
        responses:
            201:
                description: Rsvp added to event
            401:
                description: Rsvp not added to event
        """
        args = self.param.parse_args()
        if validate_params(args):
            if validate_email(args['client_email']):
                rsvp = DB.session.query(Rsvp).filter(Rsvp.event_id == event_id).filter(Rsvp.email == args['client_email']).first()
                
                if rsvp:
                    return {'success':False, 'message':'you already booked this event'}, 401

                rsvp = Rsvp(event_id, args['client_email'])
                DB.session.add(rsvp)
                try:
                    DB.session.commit()
                except IntegrityError:
                    return {'success':False, 'message':'Event does not exist'}, 401

                DB.session.refresh(rsvp)
                return {'success':True, 'payload':{'id':rsvp.id}}, 201
            return {'success': False, 'message': 'ensure that the email provided is correct'}, 401
        return {'success':False, 'message':'please ensure that you have provided all the required details'}, 401
    @jwt_required
    def put(self, event_id):
        """
        Enables users to reject or accept RSVP
        ---
        tags:
            - Rsvp V2
        parameters:
            - in: header
              name: Authorization
              description: Authorization token required for protected end points. Format should be 'Bearer token'
              type: string
              required: true
            - in: path
              name: event_id
              type: string
              required: true
            - in: formData
              name: accept_status
              type: boolean
              required: true
            - in: formData
              name: client_email
              type: string
              required: true
        responses:
            201:
                description: Rsvp accepted or rejected successfully
            401:
                description: Rsvp could not be accepted or rejected
        """
        args = self.param.parse_args()
        if validate_params(args):
            if isStringBool(args['accept_status']):
                rsvp = Rsvp.query.filter(Rsvp.event_id == event_id).filter(Rsvp.email == args['client_email']).first()
                if rsvp:
                    rsvp.accepted = args['accept_status']
                    DB.session.commit()
                    DB.session.refresh(rsvp)
                    if rsvp.accepted:
                        return {'success':True, 'payload':{'id':rsvp.id, 'status':'accepted'}}, 200
                    return {'success':True, 'payload':{'id':rsvp.id, 'status':'rejected'}}, 200
                return {'success':False, 'message':'rsvp not found'}, 401
            return {'success': False, 'message': 'invalid entry ensure that accept_status field is valid'}, 401
        return {'success':False, 'message':'please ensure that you provide all the required fields'}, 401
