"""
Module contains all the params of the requests
"""
from flask_restful import reqparse

class RegisterParams(object):
    """
    Register endpoint params
    """
    param = reqparse.RequestParser()
    param.add_argument('username', type=str, required=True, help='please provide a username')
    param.add_argument('email', type=str, required=True, help='please provide an email')
    param.add_argument('password', type=str, required=True, help='please peovide a password')
class LoginParams(object):
    """
    Login endpoint params
    """
    param = reqparse.RequestParser()
    param.add_argument('email', type=str, required=True, help='please provide an email')
    param.add_argument('password', type=str, required=True, help='please provide a password')
class LogoutParams(object):
    """
    Logout endpoint params
    """
    param = reqparse.RequestParser()
    param.add_argument('id', type=str, required=True, help='please provide an id')
class ResetParams(object):
    """
    Password reset endpoint params
    """
    param = reqparse.RequestParser()
    param.add_argument('email', type=str, required=True, help='please provide an email')
    param.add_argument('password', type=str, required=True, help='please provide a password')
class EventParams(object):
    """
    Events endpoint params
    """
    param = reqparse.RequestParser()
    param.add_argument('limit', type=int, required=False, help='ensure limit is an integer')
    param.add_argument('page', type=int, required=False, help='ensure page number is an integer')
    param.add_argument('name', type=str, required=False)
    param.add_argument('location', type=str, required=False)
    param.add_argument('host', type=int, required=False, help="ensure the host id is an integer")
    param.add_argument('time', type=str, required=False)
    param.add_argument('category', type=str, required=False)
class RsvpParams(object):
    """
    Rsvp endpoint params
    """
    param = reqparse.RequestParser()
    param.add_argument('page', required=False, type=int, help='ensure page number is an integer')
    param.add_argument('limit', type=int, required=False, help='ensure limit is an integer')
    param.add_argument('creator', required=False)
    param.add_argument('client_email', type=str, required=False)
    param.add_argument('accept_status', required=False )
class ManageRsvpParams(object):
    """
    Manage Rsvps params
    """
    param = reqparse.RequestParser()
    param.add_argument('event_id', required=True, help='please provide an event id')
    param.add_argument('action', required=True, help='please provide an action to perform')
    param.add_argument('client_email', required=True, help='please provide the client email')
class PasswordResetParams(object):
    """
    V2 reset password params
    """
    param = reqparse.RequestParser()
    param.add_argument('email', type=str, required=False)
    param.add_argument('code', type=str, required=False)
    param.add_argument('password', type=str, required=False)

class SearchParam(object):
    """
    V2 filter params
    """
    param = reqparse.RequestParser()
    param.add_argument('q', type=str, required=False)
    param.add_argument('category', type=str, required=False)
    param.add_argument('location', type=str, required=False)
class RsvpManageParams(object):
    """
    V2 rsvp manage params
    """
    param = reqparse.RequestParser()
    param.add_argument('event_id', type=str, required=False)
    param.add_argument('attendance', type=bool, required=False)