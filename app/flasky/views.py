from functools import wraps
from flask import render_template, redirect, url_for, request, flash, session
import requests
from . import flasky
def auth_required(func):
    """Wrapper to check user authorization"""
    @wraps(func)
    def auth(*args, **kargs):
        """checks for if the user is logged in through the session"""
        if not session['signed_in']:
            flash("Please log in first", 'error')
            return redirect(url_for('flasky.index'))
        return func(*args, **kargs)
    return auth

@flasky.route('/')
def index():
    return render_template('index.html')

@flasky.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        use_data = {
            'username':username,
            'email':email,
            'password':password
        }
        resp = requests.post("http://127.0.0.1:5000/api/v1/auth/register",data=use_data).json()
        if resp.get('success'):
            flash(resp.get('message'), 'error')
            return redirect(url_for('flasky.index'))
        else:
            flash(resp.get('message'), 'error')
            return redirect(url_for('flasky.index'))

@flasky.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_data = {
            'email':email,
            'password':password
        }

        resp = requests.post("http://127.0.0.1:5000/api/v1/auth/login",data=user_data).json()
        if resp.get('success'):
            session['user']=email
            session['signed_in']=True
            flash(resp.get('message'), 'error')
            return redirect(url_for('flasky.dashboard'))
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.index'))
    if request.method == 'GET':
        user_data = {
            'email':session['user']
        }
        resp = requests.get("http://127.0.0.1:5000/api/v1/auth/login", data=user_data).json()
        if resp.get('success'):
            session.pop('user')
            session['signed_in'] = False
            flash('successfully logged out', 'error')
            return redirect(url_for('flasky.index'))
        else:
            flash('could not log you out '+resp.get('message'), 'error')
            return redirect(url_for('flasky.home'))

@flasky.route('/dashboard', methods = ['GET', 'POST'])
@auth_required
def dashboard():
    resp = requests.get("http://127.0.0.1:5000/api/v1/events/"+session['user']).json()
    if resp.get('success'):
        rsvplist = []
        if request.args.get('rsvp'):
            for rsvp in request.args.get('rsvp').split(','):
                rsvplist.append(rsvp)
        return render_template("dashboard.html", data={'user':session['user'],
                            'events':resp.get('message'), 'rsvp':rsvplist})
    return render_template("dashboard.html", data={'user':session['user'],
                            'events':resp.get('message'), 'empty':True})

@flasky.route('/events', methods=['POST'])
@auth_required
def events():
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
            flash(resp.get('message'), 'error')
            return redirect(url_for('flasky.dashboard'))
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.dashboard'))

@flasky.route('/rsvps/<creator>/<event>', methods=['POST', 'GET'])
def rsvps(creator, event):
    if request.method == 'POST':
        clientmail = request.form.get('email', None)
        if clientmail is None:
            clientmail = session['user']
            resp = requests.post("http://127.0.0.1:5000/api/v1/event/"+event+"/rsvp", data={'creator':creator, 'clientEmail':clientmail}).json()
        resp = requests.post("http://127.0.0.1:5000/api/v1/event/"+event+"/rsvp", data={'creator':creator, 'clientEmail':clientmail}).json()

        if resp.get('success'):
            myrsvp = ','.join(resp.get('message'))
            flash("Rsvp sent for event "+event, 'error')
            return redirect(url_for('flasky.home'))
        else:
            flash(resp.get('message'), 'error')
            return redirect(url_for('flasky.home'))
    elif request.method == 'GET':
        resp = requests.get("http://127.0.0.1:5000/api/v1/event/"+event+"/rsvp", data={'clientEmail':session['user']}).json()
        if resp.get('success'):
            myrsvp = ','.join(resp.get('message'))
            flash("Fetched rsvp for event"+event, 'error')
            return redirect(url_for('flasky.dashboard', rsvp=myrsvp))
        else:
            flash(resp.get('message'), 'error')
            return redirect(url_for('flasky.dashboard'))

@flasky.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        resp = requests.get("http://127.0.0.1:5000/api/v1/events").json()
        if resp.get('success'):
            if resp.get('message'):
                if 'user' in session:
                    flash("Hey there welcome to Bright-Events", 'error')
                    return render_template("home.html", data = {'events':resp.get('message'), 'logged_in':True})
                flash("Hey there welcome to Bright-Events", 'error')
                return render_template("home.html", data = {'events':resp.get('message'), 'logged_in':False})
            flash("Hey there welcome to Bright-Events, There are no events at the moment", 'error')
            return render_template("home.html", data = {'events':resp.get('message'), 'logged_in':False})
        else:
            flash(resp.get("message")+" please refresh", 'error')
            return render_template("home.html", data = {'events':[]})

@flasky.route('/editevent', methods=['POST'])
def editevent():
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
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.dashboard'))
    flash(resp.get('message'), 'error')
    return redirect(url_for('flasky.dashboard'))
@flasky.route('/deleteevent/<eventname>')
def deleteevent(eventname):
    resp = requests.delete("http://127.0.0.1:5000/api/v1/events/"+eventname).json()
    if resp.get('success'):
        flash(resp.get('message'), 'error')
        return redirect(url_for('flasky.dashboard'))
    flash(resp.get('message'), 'error')
    return redirect(url_for('flasky.dashboard'))