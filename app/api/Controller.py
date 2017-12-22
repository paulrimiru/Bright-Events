"""
Module contains the controller
"""
from .models.users import Users
from .models.events import Events

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
            return {'success':True, 'payload':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}

    def loginUser(self, email, password):
        """
        logs us in
        """
        resp = self.users.getUser(email)
        if resp.get('success'):
            if password == resp.get('message').get('password'):
                return {'success':True,
                        'payload':{'username':resp.get('message').get('username'),
                                   'id':resp.get('id')}}
            return {'success':False, 'message':'user credentials wrong'}
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
                return {'success':True, 'payload':user}
            return {'success':False, 'message':'password was not reset'}
        return {'success':False, 'message':resp.get('message')}

    def addEvent(self, eventData):
        """
        creates an event
        """
        resp = self.events.create_event(eventData)
        if resp.get('success'):
            return {'success':True, 'payload':eventData}
        return {'success':False, 'message':resp.get('message')}
    def retrieveEvent(self, user_id):
        """
        retrieves events
        """
        resp = self.events.getUserEvents(user_id)
        if resp.get('success'):
            myevents = []
            for key in resp.get('message'):
                myevents.append(resp.get('message').get(key))
            return {'success':True, 'payload':myevents}
        return {'success':False, 'message':resp.get('message')}
    def retriveSingelEvent(self, user_id, event_id):
        """
        gets single event
        """
        resp = self.events.getEvent(user_id, event_id)
        print(resp)
        if resp.get("success"):
            return {'success':True, "payload":resp.get("message")}
        return {'success':False, "message":resp.get("message")}
    def deleteSingleEvent(self, email, eventname):
        """
        deletes a single event
        """
        resp = self.events.deleteEvent(email, eventname)
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
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
            return {'success':True, 'payload':EVENTLIST}
        return {'success':False, 'message':resp.get('message')}
    def addRsvp(self, user_id, event_id, email):
        """
        adds a rsvp to event
        """
        rsvpresp = self.events.rsvpEvent(user_id, event_id, email)
        if rsvpresp.get('success'):
            return {'success':True, 'payload':rsvpresp.get('message')}
        return {'success':False, 'message':rsvpresp.get('message')}
    def retriveRsvp(self, user_id, event_id):
        """
        retrieves all rsvp for single user
        """
        resp = self.events.getRsvpForEvent(user_id, int(event_id))
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return resp
    def retreiveEventsByName(self, name):
        """
        retrieves all the events with a specific name
        """
        resp = self.events.getEventByName(name)
        if len(resp) == 0:
            return {'success': False, 'message':'No events found with that name'}
        return {'success':True, 'payload':resp}
    def editEvent(self, email, name, newevent):
        """
        edits a specific event
        """
        resp = self.events.editEvent(email, name, newevent)
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}
                      