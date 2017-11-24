"""
Module contains the controller
"""
from app.Users import Users
from app.Events import Events
class Controller(object):
    """
    Class manipulates models
    """
    def __init__(self):
        self.users = Users()
        self.events = Events()
    def registerUser(self, user_data):
        """
        registers users
        """
        resp = self.users.addUser(user_data)
        if resp.get('success'):
            return {'success':True, 'message':'user registered'}
        else:
            return {'success':False, 'message':resp.get('message')}
    def loginUser(self, email, password):
        """
        logs us in
        """
        resp = self.users.getUser(email)
        if resp.get('success'):
            print(password)
            print(resp.get('message').get('password'))
            if password == resp.get('message').get('password'):
                return {'success':True, 'message':'user credentials verified'}
            else:
                return {'success':False, 'message':'user credentials wrong'}
        else:
            return {'success':False, 'message':resp.get('message')}
    def resetPassword(self, email, newPass):
        """
        resets passwords
        """
        resp = self.users.getUser(email)
        if resp.get('success'):
            user = resp.get('message')
            user['password'] = newPass
            resp = self.users.updateUser(email, user)
            if resp.get('success'):
                return {'success':True, 'message':'password reset successfully'}
            else:
                return {'success':False, 'message':'password was not reset'}
        else:
            return {'success':False, 'message':resp.get('message')}

    def addEvent(self, eventData):
        """
        creates an event
        """
        resp = self.events.create_event(eventData)
        if resp.get('success'):
            return {'success':True, 'message':'Event added'}
        else:
            return {'success':False, 'message':resp.get('message')}
    def retrieveEvent(self, email):
        """
        retrieves events
        """
        resp = self.events.getUserEvents(email)
        if resp.get('success'):
            myevents = []
            for key in resp.get('message'):
                myevents.append(resp.get('message').get(key))
            return {'success':True, 'message':myevents}
        else:
            return {'success':False, 'message':resp.get('message')}
    def retriveSingelEvent(self, email, eventname):
        """
        gets single event
        """
        resp = self.events.getEvent(email, eventname)
        if resp.get("success"):
            return {'success':True, "message":resp.get("message")}
        else:
            return {'success':False, "message":resp.get("message")}
    def deleteSingleEvent(self, email, eventname):
        """
        deletes a single event
        """
        resp = self.events.deleteEvent(email, eventname)
        if resp.get('success'):
            return {'success':True, 'message':resp.get('message')}
        else:
            return {'success':False, 'message':resp.get('message')}

    def retrieveAllEvents(self):
        """
        retrieves all events
        """
        resp = self.events.getEvents()
        if resp.get('success'):
            resp = resp.get('message')
            EVENTLIST = []
            for key in resp:
                for USEREVENT in resp.get(key):
                    EVENTLIST.append(resp.get(key).get(USEREVENT))
            return {'success':True, 'message':EVENTLIST}
        else:
            return {'success':False, 'message':resp.get('message')}
    def addRsvp(self, useremail,eventname,email):
        """
        adds a rsvp to event
        """
        rsvpresp = self.events.rsvpEvent(useremail, eventname, email)
        if rsvpresp.get('success'):
            return {'success':True, 'message':rsvpresp.get('message')}
        else:
            return {'success':False, 'message':rsvpresp.get('message')}
    def retriveRsvp(self, email, event):
        """
        retrieves all rsvp for single user
        """
        resp = self.events.getRsvpForEvent(email, event)
        return resp
                      