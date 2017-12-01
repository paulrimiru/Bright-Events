"""
This module includes all the logic triggered by endpoints
"""
from functools import wraps
from flask_restful import  Resource

from .Controller import Controller
from .utils.EndPointParams import RegisterParams, LoginParams, EventParams, ResetParams, RsvpParams

CONTROLLER = Controller()
mysession = {}
def auth_required(func):
    """Wrapper to check user authorization"""
    @wraps(func)
    def auth(*args, **kargs):
        """checks for if the user is logged in through the session"""
        if not mysession['signed_in']:
            return {"success":False,
                    'message': 'Authentication is required to access this resource'}, 401
        return func(*args, **kargs)
    return auth

class Index(Resource):
    def get(self):
        return {'success':True, 'message':'welcome to Bright Events API'}

class Register(RegisterParams, Resource):
    """
    Class provides logic for registering a user
    """
    def post(self):
        """
        listens for a post request then registers user
        """
        args = self.param.parse_args()
        user_data = {
            "username":args['username'],
            "email":args['email'],
            "password":args['password']
        }
        resp = CONTROLLER.registerUser(user_data)
        if resp.get('success'):
            return resp, 201
        return resp, 401
class Authentication(LoginParams, Resource):
    """
    Class contains logic that authenticates the users
    """
    def get(self):
        """
        Triggered by a get request and logs out the user
        """
        if 'user' in mysession:
            mysession.pop('user')
            mysession['signed_in'] = False

            return {'success':True, 'message':'user signed out'}
        return {'success':False, 'message':'Try logging in first :-)'}
    def post(self):
        """
        Triggered by a post request and logs in the user
        """
        args = self.param.parse_args()
        resp = CONTROLLER.loginUser(args['email'], args['password'])
        if resp.get('success'):
            mysession['user'] = args['email']
            mysession['signed_in'] = True
            return resp, 201
        return resp, 401
class ResetPassword(ResetParams, Resource):
    """
    Class contains logic to reset users password
    """
    def post(self):
        """
        Triggered by a post request and resets users password
        """
        args = self.param.parse_args()
        resp = CONTROLLER.resetPassword(args['email'], args['password'])
        if resp.get('success'):
            return resp, 201
        return resp, 401

class Events(EventParams, Resource):
    """
    Class contains logic to add and retrieve events
    """
    def get(self):
        """
        Triggered by get request and retrieves all events
        """
        resp = CONTROLLER.retrieveAllEvents()
        if resp.get('success'):
            return resp, 201
        return resp, 401
    @auth_required
    def post(self):
        """
        Triggered by a post request and adds the event
        """
        args = self.param.parse_args()
        event_data = {
            'name':args['name'],
            'location':args['location'],
            'category':args['category'],
            'time':args['time'],
            'creator':args['creator'],
            'rsvp':[]
        }
        resp = CONTROLLER.addEvent(event_data)
        if resp.get('success'):
            return resp, 201
        return resp, 401
    @auth_required
    def put(self):
        """
        Triggered by a put request and retrieves a single event
        """
        args = self.param.parse_args()
        resp = CONTROLLER.retreiveEventsByName(args["name"])
        if resp.get('success'):
            return resp.get('message'), 201
        return resp, 409
class ManageEvent(EventParams, Resource):
    """
    Class contains logic vto retrieveeingle events and delete events
    """
    @auth_required
    def get(self, eventId):
        resp = CONTROLLER.retrieveEvent(eventId)
        if resp.get('success'):
            return resp, 201
        return resp, 401
    
    @auth_required
    def delete(self, eventId):
        """
        triggered by a delete request and deletes event specified
        """
        resp = CONTROLLER.deleteSingleEvent(mysession['user'], eventId)
        if resp.get('success'):
            return resp, 201
        return resp, 409
    def put(self, eventId):
        """
        triggered by a put request and edits a specified event
        """
        args = self.param.parse_args()
        rsvp = CONTROLLER.retriveSingelEvent(args['creator'], eventId).get('message').get('rsvp')
        event_data = {
            'name':args['name'],
            'location':args['location'],
            'time':args['time'],
            'creator':args['creator'],
            'rsvp':rsvp
        }
        resp = CONTROLLER.editEvent(args['creator'], eventId, event_data)
        if resp.get('success'):
            return resp, 201
        return resp, 409

class Rsvp(RsvpParams, Resource):
    """
    Class manipulates Rsvp of events
    """
    def post(self, eventId):
        """
        Triggered by a post method and adds user to rsvp list
        """
        
        args = self.param.parse_args()
        resp = CONTROLLER.addRsvp(args['creator'], eventId, args['clientEmail'])
        if resp.get('success'):
            return resp, 201
        return resp, 409
    @auth_required
    def get(self, eventId):
        """
        Triggered ny get and retrieves a single rsvp
        """
        resp = CONTROLLER.retriveRsvp(mysession['user'], eventId)
        if resp.get('success'):
            return resp, 201
        return resp, 409
