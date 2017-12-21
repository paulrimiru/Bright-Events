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
    def regiser_user(self, user_data):
        """
        registers users
        """
        resp = self.users.add_user(user_data)
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}

    def login_user(self, email, password):
        """
        logs us in
        """
        resp = self.users.get_user(email)
        if resp.get('success'):
            if password == resp.get('message').get('password'):
                return {'success':True,
                        'payload':{'username':resp.get('message').get('username'),
                                   'id':resp.get('id')}}
            return {'success':False, 'message':'user credentials wrong'}
        return {'success':False, 'message':resp.get('message')}
    def reset_password(self, email, newPass):
        """
        resets passwords
        """
        resp = self.users.get_user(email)
        if resp.get('success'):
            user = resp.get('message')
            user['password'] = newPass
            resp = self.users.update_user(email, user)
            if resp.get('success'):
                return {'success':True, 'payload':user}
            return {'success':False, 'message':'password was not reset'}
        return {'success':False, 'message':resp.get('message')}

    def add_event(self, eventData):
        """
        creates an event
        """
        resp = self.events.create_event(eventData)
        if resp.get('success'):
            return {'success':True, 'payload':eventData}
        return {'success':False, 'message':resp.get('message')}
    def retrieve_event(self, user_id):
        """
        retrieves events
        """
        resp = self.events.get_user_events(user_id)
        if resp.get('success'):
            myevents = []
            for key in resp.get('message'):
                myevents.append(resp.get('message').get(key))
            return {'success':True, 'payload':myevents}
        return {'success':False, 'message':resp.get('message')}
    def retrieve_single_event(self, user_id, event_id):
        """
        gets single event
        """
        resp = self.events.get_event(user_id, event_id)
        if resp.get("success"):
            return {'success':True, "payload":resp.get("message")}
        return {'success':False, "message":resp.get("message")}
    def delete_single_event(self, user_id, event_id):
        """
        deletes a single event
        """
        resp = self.events.delete_event(user_id, event_id)
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}

    def retrieve_all_event(self):
        """
        retrieves all events
        """
        resp = self.events.get_events()
        if resp.get('success'):
            resp = resp.get('message')
            EVENTLIST = []
            for key in resp:
                for USEREVENT in resp.get(key):
                    EVENTLIST.append(resp.get(key).get(USEREVENT))
            return {'success':True, 'payload':EVENTLIST}
        return {'success':False, 'message':resp.get('message')}
    def add_rsvp(self, user_id, event_id, email):
        """
        adds a rsvp to event
        """
        rsvpresp = self.events.rsvp_event(user_id, event_id, email)
        if rsvpresp.get('success'):
            return {'success':True, 'payload':rsvpresp.get('message')}
        return {'success':False, 'message':rsvpresp.get('message')}
    def retrieve_rsvp(self, user_id, event_id):
        """
        retrieves all rsvp for single user
        """
        resp = self.events.get_rsvp_for_event(user_id, int(event_id))
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return resp
    def retrive_events_by_name(self, name):
        """
        retrieves all the events with a specific name
        """
        resp = self.events.get_event_by_name(name)
        if len(resp) == 0:
            return {'success': False, 'message':'No events found with that name'}
        return {'success':True, 'payload':resp}
    def edit_event(self, user_id, event_id, newevent):
        """
        edits a specific event
        """
        resp = self.events.edit_event(user_id, event_id, newevent)
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}
    def accept_rsvp(self, userId, eventId, clientEmail):
        resp = self.events.confirm_rsvp(userId, eventId, clientEmail)
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}
    def reject_rsvp(self, userId, eventId, clientEmail):
        resp = self.events.reject_rsvp(userId, eventId, clientEmail)
        if resp.get('success'):
            return {'success':True, 'payload':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}              