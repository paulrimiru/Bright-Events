"""
Module contains Events model
"""
class Events(object):
    """
    class contains methods that manipulates event models
    """
    def __init__(self):
        self.events_dict = {}
    def create_event(self, eventData):
        """
        creates events
        """
        name = eventData.get('name')
        if eventData.get('creator') and eventData.get('name'):
            if 'creator' in eventData:
                creator = eventData.get('creator')
                if creator in self.events_dict:
                    if name in self.events_dict.get(creator):
                        return {'success':False,
                                'message':'Duplicate event, choose a different name'}
                    user_events = self.events_dict.get(creator)
                    user_events.update({name:eventData})
                    return {'success':True, 'message':'Event succesfully added'}
                new_event = {creator:{name:eventData}}
                self.events_dict.update(new_event)
                return {'success':True, 'message':'First Event added, Hurray!!'}
            return {'success':False, 'message':'no user field provided'}
        return {'success':False,
                'message':'ensure you have the event name and your email filled'}

    def getEvents(self):
        """
        gets all evennts
        """
        return {'success':True, 'message':self.events_dict}
    def getEventByName(self, name):
        """
        gets a all events with given name
        """
        result = []
        for user in self.events_dict:
            for event in self.events_dict.get(user):
                if name == self.events_dict.get(user).get(event).get('name'):
                    result.append(self.events_dict.get(user))
        return {'success': True, 'message': result}

    def getUserEvents(self, userEmail):
        """
        gets a users events
        """
        if self.events_dict.get(userEmail):
            return {'success':True, 'message':self.events_dict.get(userEmail)}
        return {'success':False, 'message':'No events for this user'}
    def deleteEvent(self, userEmail, eventName):
        """
        deletes an event
        """
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                self.events_dict.get(userEmail).pop(eventName)
                return {'success':True, 'message':'Event deleted'}
            return {'success':False, 'message':'Event not found'}
        return {'success':False, 'message':'user does not have any events'}
    def getEvent(self, userEmail, eventName):
        """
        gets specific event
        """
        resp = self.getUserEvents(userEmail)
        if resp.get('success'):
            if resp.get('message').get(eventName):
                return {'success':True, 'message':resp.get('message').get(eventName)}
            return {'success':False, 'message':'event does not exist'}
        return {'success':False, 'message':resp.get('message')}
    def editEvent(self, userEmail, eventName, new_event):
        """
        edits specific event
        """
        resp = self.deleteEvent(userEmail, eventName)
        if resp.get('success'):
            resp = self.create_event(new_event)
            if resp.get('success'):
                return {'success':True, 'message':'Event successfully edited'}
            return {'success':False, 'message':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}

    def rsvpEvent(self, userEmail, eventName, clientEmail):
        """
        adds rsvpto event
        """
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                rsvp = self.events_dict.get(userEmail).get(eventName).get('rsvp')
                if clientEmail not in rsvp:
                    rsvp.append(clientEmail)
                    return {'success':True, 'message':rsvp}
                return {'success':False, 'message':"You already Reserved this event"}
            return {'success':False, 'message':"cannot find the event"}
        return {'success':False, 'message':"user does not exist"}
    def getRsvpForEvent(self, userEmail, eventName):
        """
        gets all the rsvp for event
        """
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                resp = self.events_dict.get(userEmail).get(eventName).get('rsvp')
                return {'success':True, 'message':resp}
            return {'success':False, 'message':"cannot find the event"}
        return {'success':False, 'message':'user does not exist'}
