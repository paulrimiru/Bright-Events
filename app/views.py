"""
This module includes all the logic triggered by endpoints
"""
from functools import wraps
from app.Controller import Controller
from app.EndPointParams import RegisterParams, LoginParams, EventParams, ResetParams, RsvpParams

from flask_restful import  Resource
from flask import session


CONTROLLER = Controller()

def auth_required(func):
    """Wrapper to check user authorization"""
    @wraps(func)
    def auth(*args, **kargs):
        """checks for if the user is logged in through the session"""
        if not session['signed_in']:
            return {"success":False,
                    'message': 'Authentication is required to access this resource'}, 401
        return func(*args, **kargs)
    return auth

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
        else:
            return resp, 401
class Authentication(LoginParams, Resource):
    """
    Class contains logic that authenticates the users
    """
    def get(self):
        """
        Triggered by a get request and logs out the user
        """
        if 'user' in session:
            session.pop('user')
            session['signed_in'] = False

            return {'success':True, 'message':'user signed out'}
        else:
            return {'success':False, 'message':'Try logging in first :-)'}
    def post(self):
        """
        Triggered by a post request and logs in the user
        """
        args = self.param.parse_args()
        resp = CONTROLLER.loginUser(args['email'], args['password'])
        if resp.get('success'):
            session['user'] = args['email']
            session['signed_in'] = True
            return resp, 201
        else:
            return resp, 401
class ResetPassword(ResetParams, Resource):
    """
    Class contains logic to reset users password
    """
    @auth_required
    def post(self):
        """
        Triggered by a post request and resets users password
        """
        args = self.param.parse_args()
        resp = CONTROLLER.resetPassword(args['email'], args['password'])
        if resp.get('success'):
            return resp, 201
        else:
            return resp, 401

class CreateEvent(EventParams, Resource):
    """
    Class contains logic to add and retrieve events
    """
    @auth_required
    def get(self):
        """
        Triggered by get request and retrieves all events
        """
        resp = CONTROLLER.retrieveAllEvents()
        if resp.get('success'):
            return resp, 201
        else:
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
            'time':args['time'],
            'creator':args['creator'],
            'rsvp':[]
        }
        resp = CONTROLLER.addEvent(event_data)
        if resp.get('success'):
            return resp, 201
        else:
            return resp, 401
class Event(Resource):
    """
    Class contains logic vto retrieveeingle events and delete events
    """
    @auth_required
    def put(self, eventId):
        """
        Triggered by a put request and retrieves a single event
        """
        resp = CONTROLLER.retriveSingelEvent(session['user'], eventId)
        if resp.get('success'):
            return resp, 201
        else:
            return resp, 409
    @auth_required
    def delete(self, eventId):
        """
        triggered by a delete request and deletes event specified
        """
        resp = CONTROLLER.deleteSingleEvent(session['user'], eventId)
        if resp.get('success'):
            return resp, 201
        else:
            return resp, 409
class Rsvp(RsvpParams, Resource):
    """
    Class manipulates Rsvp of events
    """
    @auth_required
    def post(self, eventId):
        """
        Triggered by a post method and adds user to rsvp list
        """
        args = self.param.parse_args()
        resp = CONTROLLER.addRsvp(session['user'], eventId, args['clientEmail'])
        if resp.get('success'):
            return resp, 201
        else:
            return resp, 409
    @auth_required
    def get(self, eventId):
        """
        Triggered ny get and retrieves a single rsvp
        """
        args = self.param.parse_args()
        resp = CONTROLLER.retriveRsvp(args['clientEmail'], eventId)
        if resp.get('success'):
            return resp, 201
        else:
            return resp, 409