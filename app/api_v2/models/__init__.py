from datetime import datetime, timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import uuid

BCRYPT = Bcrypt()
DB = SQLAlchemy()
JWTMANAGER = JWTManager()

class User(DB.Model):
    """
    User model
    """
    id = DB.Column(DB.Integer(), primary_key=True)
    username = DB.Column(DB.String(255))
    email = DB.Column(DB.String(255), unique=True)
    password = DB.Column(DB.Binary(255))
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
    user_id = DB.Column(DB.Integer(), DB.ForeignKey('user.id'))
    code = DB.Column(DB.String(255), unique=True, default=generate_uniquecode)
    date = DB.Column(DB.DateTime(), default=expiration_date)

    user = DB.relationship(User)
    DB.UniqueConstraint('user_id', 'code', name='uni_user_code')

    def __init__(self, user):
        self.user = user

class Event(DB.Model):
    id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(255))
    location = DB.Column(DB.String(255))
    host = DB.Column(DB.Integer(), DB.ForeignKey('user.id'), nullable=False)
    category = DB.Column(DB.Integer(), DB.ForeignKey('category.id'), nullable=False)
    date = DB.Column(DB.DateTime())

    def __init__(self, name, location, host, category, date):
        self.name = name
        self.location = location
        self.host = host
        self.category = category
        self.date = date
class Category(DB.Model):
    id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(), nullable=False)

    def __init__(self, name):
        self.name = name