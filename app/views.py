from functools import wraps
from flask import session, render_template, redirect, url_for, request, flash

from app import APP
from app.Categories import Categories
from app.Controller import Controller


controller = Controller()
categories = Categories()

def auth(func):
    @wraps(func)
    def auth(*args, **kargs):
        if 'signed_in' not in session:
            flash("You are not logged in", 'error')
            return redirect(url_for('index'))
        return func(*args, **kargs)
    return auth
@APP.route('/')
@APP.route('/index')
def index():
    return render_template('index.html')
@APP.route('/dashboard')
@auth
def dashboard():
    events = controller.retrieveEvent(session['user_email'])
    return render_template('dashboard', data=events)
@APP.route('/api/auth/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_confirm = request.form['password-confirm']
        user_data = {
            'username':username,
            'password':password,
            'email':email
        }

        if controller.registerUser(user_data).get('success'):
            flash("user registered succesfully please sign in")
            return redirect(url_for('index'))
        else:
            flash("user registered not successful")
            return redirect(url_for('index'))


@APP.route('/api/auth/login', methods=['POST', 'GET'])
def login():
    pass
@APP.route('/api/auth/reset-password')
def resetPassword():
    pass
@APP.route('/api/events', methods=['POST', 'GET'])
@auth
def events():
    pass
@APP.route('/api/events/<eventId>')
@auth
def event(eventId):
    pass
@APP.route('/api/events')
@auth
def getEvents():
    pass
@APP.route('/api/event/<eventId>/rsvp')
@auth
def rsvp(eventId):
    pass