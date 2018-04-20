from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from marshmallow import fields, Schema
from flask_mail import Mail
from sqlalchemy import event

import uuid

BCRYPT = Bcrypt()
DB = SQLAlchemy()
JWTMANAGER = JWTManager()
MAIL = Mail()

class Users(DB.Model):
    """
    User model
    """
    id = DB.Column(DB.Integer(), primary_key=True)
    username = DB.Column(DB.String(255))
    email = DB.Column(DB.String(255), unique=True)
    password = DB.Column(DB.Binary(255))
    date_created = DB.Column(DB.DateTime(), default=datetime.now())
    date_modified = DB.Column(DB.DateTime(), default=datetime.now())
    events = DB.relationship('Event', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.encrypt_password(password)

    def encrypt_password(self, password):
        """encrypts the password"""
        self.password = BCRYPT.generate_password_hash(password)
def generate_uniquecode():
    """method returns a unique code as string"""
    return str(uuid.uuid4())
def expiration_date():
    """Sets the expiration date"""
    return datetime.now() + timedelta(days=1)
class ResetPassword(DB.Model):
    """model for the password reset table"""
    id = DB.Column(DB.Integer(), primary_key=True)
    user_id = DB.Column(DB.Integer(), DB.ForeignKey('users.id'))
    code = DB.Column(DB.String(255), unique=True, default=generate_uniquecode)
    date = DB.Column(DB.DateTime(), default=expiration_date)

    user = DB.relationship(Users)
    DB.UniqueConstraint('user_id', 'code', name='uni_user_code')

    def __init__(self, user):
        self.user = user

class Event(DB.Model):
    """model for user table"""
    id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(255))
    location = DB.Column(DB.String(255))
    host = DB.Column(DB.Integer(), DB.ForeignKey('users.id'), nullable=False)
    category = DB.Column(DB.String(), nullable=False)
    date = DB.Column(DB.DateTime())
    private = DB.Column(DB.Boolean())
    rsvps = DB.relationship('Rsvp', backref='event', lazy=True)
    date_created = DB.Column(DB.DateTime())
    date_modified = DB.Column(DB.DateTime())


    def __init__(self, name, location, host, category, date, private=False):
        self.name = name
        self.location = location
        self.host = host
        self.category = category
        self.date = date
        self.private = private
class EventSchema(Schema):
    """shchema for events"""
    id = fields.Int(dump_only = True)
    name = fields.Str()
    location = fields.Str()
    host = fields.Str()
    date = fields.Date(dt_format='iso8601')
    category = fields.Str()
    is_private = fields.Bool()

event_schema = EventSchema(many=False)
events_schema = EventSchema(many=True)


class Rsvp(DB.Model):
    """model for rsvp table"""
    id = DB.Column(DB.Integer(), primary_key=True)
    event_id = DB.Column(DB.Integer(), DB.ForeignKey('event.id'), nullable=False)
    email = DB.Column(DB.String(255))
    accepted = DB.Column(DB.Boolean(), default=True)
    date_created = DB.Column(DB.DateTime(), default=datetime.now())
    date_modified = DB.Column(DB.DateTime(), default=datetime.now())

    def __init__(self,event_id, email, accepted=True):
        self.event_id = event_id
        self.email = email
        self.accepted = accepted
class RsvpSchema(Schema):
    """schema for rsvps"""
    id = fields.Int(dump_only=True)
    event_id = fields.Int(as_string=True)
    email = fields.Str()
    accepted = fields.Bool()

    
rsvps_schema = RsvpSchema(many=True)
rsvp_schema = RsvpSchema()

class TokenBlackList(DB.Model):
    """model for token blacklist table"""
    id = DB.Column(DB.Integer, primary_key=True)
    token = DB.Column(DB.String(), nullable=False)
    user_id = DB.Column(DB.Integer(), nullable=False)
    expiry_date = DB.Column(DB.DateTime(), nullable=False)
    def __init__(self, token, user_id, expiry_date):
        self.token = token
        self.user_id = user_id
        self.expiry_date = expiry_date
class TokenBlacklistSchema(Schema):
    """schem afor token blacklist"""
    id = fields.Int(dump_only=True)
    token = fields.Str()
    user_id = fields.Str()
    expiration_date = fields.Date(dt_format='iso8601')

token_schema = TokenBlacklistSchema()
tokens_schema = TokenBlacklistSchema(many = True)

@event.listens_for(Event, 'before_insert')
def update_create_and_modified(mapper, connection, target):
    target.date_created = datetime.utcnow()
    target.date_modified = datetime.utcnow()
@event.listens_for(Event, 'before_update')
def update_modified(mapper, connection, target):
    target.date_modified = datetime.utcnow()