from app.Users import Users
from app.Events import Events
from app.Categories import Categories
class Controller(object):
    def __init__(self):
        self.users = Users()
        self.events = Events()
    def registerUser(self, user_data):
        resp = self.users.addUser(user_data)
        if resp.get('success'):
            return {'success':True, 'message':'user registered'}
        else:
            return {'success':False, 'message':resp.get('message')}
    def loginUser(self, email, password):
        resp = self.users.getUser(email)
        if resp.get('success'):
            if password is resp.get('message').get('password'):
                return {'success':True, 'message':'user credentials verified'}
            else:
                return {'success':False, 'message':'user credentials wrong'}
        else:
            return {'success':False, 'message':resp.get('message')}
    def addEvent(self, eventData):
        resp = self.events.create_event(eventData)
        if resp.get('success'):
            return {'success':True, 'message':'Event added'}
        else:
            return {'success':False, 'message':resp.get('message')}
    def retrieveEvent(self, email):
        resp = self.events.getUserEvents(email)
        if resp.get('success'):
            myevents = []
            for key in resp.get('message'):
                myevents.append(resp.get('message').get(key))
            return {'success':True, 'message':myevents}
        else:
            return {'success':False, 'message':resp.get('message')}
    def retrieveAllEvents(self):
        resp = self.events.getEvents()
        if resp.get('success'):
            resp = resp.get('message')
            eventList = []
            for key in resp:
                for userEvent in resp.get(key):
                    eventList.append(resp.get(key).get(userEvent))
            return {'success':True, 'message':eventList}
        else:
            return {'success':False, 'message':resp.get('message')}
    def addRsvp(self, useremail,eventname,email):
        rsvpresp = self.events.rsvpEvent(useremail, eventname, email)
        if rsvpresp.get('success'):
            return {'success':True, 'message':rsvpresp.get('message')}
        else:
            return {'success':False, 'message':rsvpresp.get('message')}
    def retriveRsvp(self, email, event):
        resp = self.events.getRsvpForEvent(email, event)
        return resp
                      