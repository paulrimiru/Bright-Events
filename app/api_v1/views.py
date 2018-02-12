"""
This module includes all the logic triggered by endpoints
"""
from functools import wraps
from flask_restful import  Resource

from .controller import Controller
from .utils.endpointparams import RegisterParams, LoginParams, EventParams
from .utils.endpointparams import ResetParams, RsvpParams, LogoutParams, ManageRsvpParams

import re
CONTROLLER = Controller()
MYSESSION = {}
def auth_required(func):
    """Wrapper to check user authorization"""
    @wraps(func)
    def auth(*args, **kargs):
        """checks for if the user is logged in through the session"""
        if 'signed_in' not in MYSESSION or not MYSESSION['signed_in']:
            return {"success":False,
                    'message': 'Authentication is required to access this resource'}, 302
        return func(*args, **kargs)
    return auth
def validate_email(email):
    """checks if email is valid"""
    regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if regex.match(email):
        return True
    return False
def validate_password(password):
    """checks for strong password"""
    if len(password) < 6:
        return False
    return True
class Index(Resource):
    """Resource for applicaion introduction"""
    def get(self):
        """
        Introduction to the Bright-Events API
        ---
        tags:
            - Introduction
        responses:
            200:
                description: Introduction to the Bright-Events API
        """
        return {'success':True, 'message':'welcome to Bright Events API'}, 200

class Register(RegisterParams, Resource):
    """Resouce handles user registratiion"""
    def post(self):
        """
        Register users
        ---
        tags:
            - Registration
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
        """
        args = self.param.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        if not validate_email(email):
            return {'success':False, 'message':'invalid email'}, 409
        if not validate_password(password):
            return {'success':False,
                    'message':'your password is weak, enter a password with 6 characters'}, 409

        user_data = {
            "username":username,
            "email":email,
            "password":password
        }
        resp = CONTROLLER.register_user(user_data)
        if resp.get('success'):
            return resp, 201
        return resp, 409

class Authentication(LoginParams, Resource):
    """
    Class contains logic that authenticates the users
    """
    def post(self):
        """
        Login users
        ---
        tags:
            - Authentication
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
            409:
                description: User credentials are wrong
        """
        args = self.param.parse_args()
        resp = CONTROLLER.login_user(args['email'], args['password'])
        if resp.get('success'):
            MYSESSION['user'] = resp.get('payload').get('id')
            MYSESSION['signed_in'] = True
            return resp, 201
        return resp, 409
class Logout(LogoutParams, Resource):
    """
    class contains logic that logsout user
    """
    def post(self):
        """
        Logout users
        ---
        tags:
            - Authentication
        parameters:
            - in: formData
              name: id
              type: string
              required: true
        responses:
            201:
                description: User logged out
            408:
                description: Id provided is not logged in
            409:
                description: No user logged in at the momment
        """
        args = self.param.parse_args()
        if 'user' in MYSESSION:
            if MYSESSION['user'] == int(args['id']):
                MYSESSION.pop('user')
                MYSESSION['signed_in'] = False
                return {'success':True, 'payload':None}, 201
            return {'success':False, 'message':'user provided is not in session'}, 408
        return {'success':False, 'message':'No user is logged i \
                at the momment with your account'}, 409
class ResetPassword(ResetParams, Resource):
    """
    Class resets users passwords
    """
    def post(self):
        """
        Reset users password
        ---
        tags:
            - Authentication
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
                description: Password changed
            409:
                description: User credentials are wrong
        """
        args = self.param.parse_args()
        resp = CONTROLLER.reset_password(args['email'], args['password'])
        if resp.get('success'):
            return resp, 201
        return resp, 409

class Events(EventParams, Resource):
    """
    Class contains logic to add and retrieve events
    """
    def get(self):
        """
        Retreive all events
        ---
        tags:
            - Events
        responses:
            201:
                description: Events retrieved
            409:
                description: Events couldnot be retrieved
        """
        resp = CONTROLLER.retrieve_all_events()
        if resp.get('success'):
            return resp, 201
        return resp, 409
    @auth_required
    def post(self):
        """
        Create event
        ---
        tags:
            - Events
        parameters:
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
              name: creator
              type: string
              required: true
            - in: formData
              name: rsvp
              type: list
              required: false
        responses:
            201:
                description: Event created successfully
            409:
                description: Event not created
        """
        args = self.param.parse_args()
        event_data = {
            'name':args['name'],
            'location':args['location'],
            'category':args['category'],
            'time':args['time'],
            'creator':MYSESSION['user'],
            'rsvp':[]
        }
        resp = CONTROLLER.add_event(event_data)
        if resp.get('success'):
            return resp, 201
        return resp, 409
    @auth_required
    def put(self):
        """
        Retrieve specific event by name
        ---
        tags:
            - Events
        parameters:
            - in: formData
              name: name
              type: string
              required: true
        responses:
            201:
                description: Event retrieved
            409:
                description: Event could not be retrieved
        """
        args = self.param.parse_args()
        resp = CONTROLLER.retrieve_events_by_name(args["name"])
        if resp.get('success'):
            return resp.get('message'), 201
        return resp, 409
class ManageEvent(EventParams, Resource):
    """
    Class contains logic vto retrieveeingle events and delete events
    """
    @auth_required
    def get(self, event_id):
        """
        Retrieve specific Event
        ---
        tags:
            - Events
        parameters:
            - in: path
              name: event_id
              type: int
              required: true
        responses:
            201:
                description: Event retrieved successfully
            409:
                description: Event could not be found
        """
        if event_id:
            resp = CONTROLLER.retrieve_single_event(int(MYSESSION['user']), int(event_id))
            if resp.get('success'):
                return resp, 201
        resp = CONTROLLER.retrieve_event(int(MYSESSION['user']))
        if resp.get('success'):
            print(resp)
            return resp, 201
        return resp, 409

    @auth_required
    def delete(self, event_id):
        """
        Delete specific Event
        ---
        tags:
            - Events
        parameters:
            - in: path
              name: event_id
              type: int
              required: true
        responses:
            201:
                description: Event deleted successfully
            409:
                description: Event could not be deleted
        """
        resp = CONTROLLER.delete_single_event(MYSESSION['user'], int(event_id))
        if resp.get('success'):
            return resp, 201
        return resp, 409
    def put(self, event_id):
        """
        Edit specific Event
        ---
        tags:
            - Events
        parameters:
            - in: path
              name: event_id
              type: int
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
              name: creator
              type: string
              required: true
            - in: formData
              name: rsvp
              type: list
              required: false
        responses:
            201:
                description: Specific event edited successfully
            409:
                description: Event could not be edited
        """
        args = self.param.parse_args()
        rsvp = CONTROLLER.retrieve_single_event(MYSESSION['user'],
                                                int(event_id)).get('payload').get('rsvp')
        event_data = {
            'name':args['name'],
            'location':args['location'],
            'time':args['time'],
            'creator':MYSESSION['user'],
            'rsvp':rsvp
        }
        resp = CONTROLLER.edit_event(MYSESSION['user'], int(event_id), event_data)
        if resp.get('success'):
            return resp, 201
        return resp, 409

class Rsvp(RsvpParams, Resource):
    """
    Class manipulates Rsvp of events
    """
    def post(self, event_id):
        """
        Rsvp a particular event
        ---
        tags:
            - Events
        parameters:
            - in: path
              name: event_id
              type: int
              required: true
            - in: formData
              name: creator
              type: string
              required: true
            - in: formData
              name: client_email
              type: string
              required: true
        responses:
            201:
                description: Rsvp added to event
            409:
                description: Rsvp not added to event
        """
        args = self.param.parse_args()
        email = args['client_email']
        creator = args['creator']
        if not validate_email(email):
            return {'success':False, 'message':'invalid email'}, 409
        resp = CONTROLLER.add_rsvp(int(creator), int(event_id), email)
        if resp.get('success'):
            return resp, 201
        return resp, 409
    @auth_required
    def get(self, event_id):
        """
        Retrieve Rsvp for a particular event
        ---
        tags:
            - Rsvp
        parameters:
            - in: path
              name: event_id
              type: int
              required: true
        responses:
            201:
                description: Rsvp retrived successfully
            409:
                description: Rsvp not added to event
        """
        resp = CONTROLLER.retrieve_rsvp(MYSESSION['user'], event_id)
        if resp.get('success'):
            return resp, 201
        return resp, 409
class ManageRsvp(ManageRsvpParams, Resource):
    """
    Class manages Rsvp for a user
    """
    @auth_required
    def put(self):
        """
        Enables users to reject or accept RSVP
        ---
        tags:
            - Rsvp
        parameters:
            - in: formData
              name: event_id
              type: string
              required: true
            - in: formData
              name: action
              type: string
              required: true
            - in: formData
              name: client_email
              type: string
              required: true
        responses:
            201:
                description: Rsvp accepted or rejected successfully
            409:
                description: Rsvp could not be accepted or rejected
        """
        args = self.param.parse_args()
        event_id = args['event_id']
        action = args['action']
        client_email = args['client_email']
        if action == 'cancel':
            resp = CONTROLLER.reject_rsvp(MYSESSION['user'], int(event_id), client_email)
            if resp.get('success'):
                return resp, 201
            return resp, 409
        resp = CONTROLLER.accept_rsvp(MYSESSION['user'], int(event_id), client_email)
        if resp.get('success'):
            return resp, 201
        return resp, 409
        
