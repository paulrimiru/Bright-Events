"""
Module contains all the routes and logic for flask app
"""
from functools import wraps
from flask import render_template, redirect, url_for, request, flash, session
import requests
from . import flasky
def auth_required(func):
    """Wrapper to check user authorization"""
    @wraps(func)
    def auth(*args, **kargs):
        """checks for if the user is logged in through the session"""
        if 'signed_in' not in session or not session['signed_in']:
            flash("Please log in first", 'error')
            return redirect(url_for('flasky.index'))
        return func(*args, **kargs)
    return auth

@flasky.route('/')
def index():
    """
    Renders landing page
    """
    return render_template('index.html')

@flasky.route('/register', methods=['POST'])
def register():
    """
    registers users
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        use_data = {
            'username':username,
            'email':email,
            'password':password
        }
        resp = requests.post("http://127.0.0.1:5000/api/v1/auth/register", data=use_data).json()
        if resp.get('success'):
            flash("Account created successfully", 'error')
<<<<<<< HEAD
=======
            return redirect(url_for('flasky.index'))
        else:
            flash(resp.get('message'), 'error')
>>>>>>> 8deb555786fe3fd5ed2ccb44af5eadfe2edb090d
            return redirect(url_for('flasky.index'))
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.index'))

@flasky.route('/login', methods=['GET', 'POST'])
def login():
    """
    logs in users
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_data = {
            'email':email,
            'password':password
        }

        resp = requests.post("http://127.0.0.1:5000/api/v1/auth/login", data=user_data).json()
        if resp.get('success'):
            session['user'] = resp.get('payload').get('id')
            session['username'] = resp.get('payload').get('username')
            session['email'] = email
            session['signed_in'] = True
            flash("Welcome " + resp.get('payload').get('username'), 'success')
            return redirect(url_for('flasky.dashboard'))
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.index'))
    if request.method == 'GET':
        user_data = {
            'id':session['user']
        }
        resp = requests.post("http://127.0.0.1:5000/api/v1/auth/logout", data=user_data).json()
        if resp.get('success'):
            session.pop('user')
            session.pop('username')
            session.pop('email')
            session['signed_in'] = False
            flash('successfully logged out', 'success')
            return redirect(url_for('flasky.index'))
        flash('could not log you out '+resp.get('message'), 'error')
        return redirect(url_for('flasky.home'))

@flasky.route('/dashboard', methods=['GET', 'POST'])
@auth_required
def dashboard():
    """
    renders dashboard
    """
    resp = requests.get("http://127.0.0.1:5000/api/v1/events/"+str(session['user'])).json()
    if resp.get('success'):
        rsvplist = []
        if request.args.get('rsvp'):
            for rsvp in request.args.get('rsvp').split(','):
                rsvplist.append(rsvp)
        return render_template("dashboard.html", data={'user':session['username'],
                                                       'events':resp.get('payload'),
                                                       'rsvp':rsvplist})
    return render_template("dashboard.html", data={'user':session['username'],
                                                   'events':resp.get('payload'),
                                                   'empty':True})

@flasky.route('/events', methods=['POST'])
@auth_required
def events():
    """
    Adds events and retrieves all events
    """
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        category = request.form['category']
        date = request.form['time']

        event_data = {
            'name':name,
            'location':location,
            'category':category,
            'creator':session['user'],
            'time':date
        }
        resp = requests.post("http://127.0.0.1:5000/api/v1/events", data=event_data).json()
        if resp.get('success'):
            flash("Event has been saved successfully", 'success')
            return redirect(url_for('flasky.dashboard'))
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.dashboard'))

@flasky.route('/rsvps/<creator>/<event>', methods=['POST', 'GET'])
def rsvps(creator, event):
    """
    adds rsvp and  retrieves rsvp
    """
    if request.method == 'POST':
        clientmail = request.form.get('email', None)
        if not clientmail:
            clientmail = session['email']
<<<<<<< HEAD
        resp = requests.post("http://127.0.0.1:5000/api/v1/event/"+event+"/rsvp",
                             data={'creator':creator, 'clientEmail':clientmail}).json()
=======
        resp = requests.post("http://127.0.0.1:5000/api/v1/event/"+event+"/rsvp", data={'creator':creator, 'clientEmail':clientmail}).json()
>>>>>>> 8deb555786fe3fd5ed2ccb44af5eadfe2edb090d

        if resp.get('success'):
            myrsvp = ','.join(resp.get('payload'))
            flash("Rsvp sent for event "+event, 'error')
            return redirect(url_for('flasky.home'))
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.home'))
    elif request.method == 'GET':
        resp = requests.get("http://127.0.0.1:5000/api/v1/event/"+event+"/rsvp",
                            data={'clientEmail':session['user']}).json()
        if resp.get('success'):
            myrsvp = ','.join(resp.get('payload'))
            flash("Fetched rsvp for event"+event, 'error')
            return redirect(url_for('flasky.dashboard', rsvp=myrsvp))
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.dashboard'))

@flasky.route('/home', methods=['POST', 'GET'])
def home():
    """
    REnders the home page
    """
    if request.method == 'GET':
        resp = requests.get("http://127.0.0.1:5000/api/v1/events").json()
        if resp.get('success'):
            if resp.get('payload'):
                if 'user' in session:
                    flash("Hey there, "+ session['username'] +" welcome to Bright-Events", 'error')
<<<<<<< HEAD
                    return render_template("home.html",
                                           data={'events':resp.get('payload'),
                                                 'logged_in':True, 'id':session['user']})
                flash("Hey there Anonymous welcome to Bright-Events", 'error')
                return render_template("home.html", data={'events':resp.get('payload'),
                                                          'logged_in':False, 'id':0})
            if 'user' in session:
                flash("Hey there, "+
                      session['username'] +
                      " welcome to Bright-Events, There are no events at the moment", 'error')
                return render_template("home.html", data={'events':resp.get('payload'),
                                                          'logged_in':True, 'id':session['user']})
            flash("Hey there, Anonymous welcome to Bright-Events, There are no events at the moment"
                  , 'error')
            return render_template("home.html", data={'events':resp.get('payload'),
                                                      'logged_in':False, 'id':0})
        flash(resp.get("message")+" please refresh", 'error')
        return render_template("home.html", data={'events':[], 'id':0})
=======
                    return render_template("home.html", data = {'events':resp.get('payload'), 'logged_in':True, 'id':session['user']})
                flash("Hey there Anonymous welcome to Bright-Events", 'error')
                return render_template("home.html", data = {'events':resp.get('payload'), 'logged_in':False,'id':0})
            if 'user' in session:
                flash("Hey there, "+ session['username'] +" welcome to Bright-Events, There are no events at the moment", 'error')
                return render_template("home.html", data = {'events':resp.get('payload'), 'logged_in':True, 'id':session['user']})
            flash("Hey there, Anonymous welcome to Bright-Events, There are no events at the moment", 'error')
            return render_template("home.html", data = {'events':resp.get('payload'), 'logged_in':False, 'id':0})
        else:
            flash(resp.get("message")+" please refresh", 'error')
            return render_template("home.html", data = {'events':[], 'id':0})
>>>>>>> 8deb555786fe3fd5ed2ccb44af5eadfe2edb090d

@flasky.route('/editevent', methods=['POST'])
def editevent():
    """
    Edits events
    """
    orginalname = request.form['originalname']
    name = request.form['name']
    location = request.form['location']
    category = request.form['category']
    date = request.form['time']
    event_data = {
        'name':name,
        'location':location,
        'category':category,
        'creator':session['user'],
        'time':date
    }
    resp = requests.put("http://127.0.0.1:5000/api/v1/events/"+orginalname, data=event_data).json()
    if resp.get('success'):
        flash("Edited event successfully", 'error')
        return redirect(url_for('flasky.dashboard'))
    flash(resp.get('message'), 'error')
    return redirect(url_for('flasky.dashboard'))
@flasky.route('/deleteevent/<eventname>')
def deleteevent(eventname):
    """
    Deletes events
    """
    resp = requests.delete("http://127.0.0.1:5000/api/v1/events/"+eventname).json()
    if resp.get('success'):
        flash(resp.get('payload'), 'error')
        return redirect(url_for('flasky.dashboard'))
    flash(resp.get('message'), 'error')
    return redirect(url_for('flasky.dashboard'))
