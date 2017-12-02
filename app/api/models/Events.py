"""
Module contains Events model
"""
class Events(object):
    """
    class contains methods that manipulates event models
    """
    def __init__(self):
        self.events_dict = {}
    def create_event(self, eventData, event_id=0):
        """
        creates events
        """
        event_id = self.generate_id(eventData, event_id)
        if event_id:
            user_events = self.events_dict.get(eventData.get('creator'))            
            for events in user_events:
                if eventData.get('name') == user_events.get(events).get('name'):
                    return {'success':False,
                            'message':"Dublicate event, please change the event name"}
            user_events.update({event_id:eventData})
            self.events_dict.update({eventData.get('creator'):user_events})
            return {'success':True, 'message':{event_id:eventData}}
        else:
            return {'success':False, 'message': 'please provide the creator user id'}

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
        for user_id in self.events_dict:
            user_events = self.events_dict.get(user_id)
            for event_id in user_events:
                if name == user_events.get(event_id).get('name'):
                    result.append(user_events.get(event_id))
        return {'success': True, 'message': result}

    def getUserEvents(self, user_id):
        """
        gets a users events
        """
        if user_id in self.events_dict:
            if self.events_dict.get(user_id):
                return {'success':True, 'message':self.events_dict.get(user_id)}
            return {'success':False, 'message':'No events for this user'}
        return {'success':False, 'message':'No user in events'}
    def deleteEvent(self, user_id, event_id):
        """
        deletes an event
        """
        if user_id in self.events_dict:
            if event_id in self.events_dict.get(user_id):
                self.events_dict.get(user_id).pop(event_id)
                return {'success':True, 'message':'Event deleted'}
            return {'success':False, 'message':'Event not found'}
        return {'success':False, 'message':'user does not have any events'}
    def getEvent(self, user_id, event_id):
        """
        gets specific event
        """
        resp = self.getUserEvents(user_id)
        print(resp)
        if resp.get('success'):
            if resp.get('message').get(event_id):
                return {'success':True, 'message':resp.get('message').get(event_id)}
            return {'success':False, 'message':'event does not exist'}
        return {'success':False, 'message':resp.get('message')}
    def editEvent(self, user_id, event_id, new_event):
        """
        edits specific event
        """
        resp = self.deleteEvent(user_id, event_id)
        if resp.get('success'):
            resp = self.create_event(new_event, event_id)
            if resp.get('success'):
                return {'success':True, 'message':new_event}
            return {'success':False, 'message':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}

    def rsvpEvent(self, user_id, event_id, clientEmail):
        """
        adds rsvpto event
        """
        if user_id in self.events_dict:
            if int(event_id) in self.events_dict.get(user_id):
                rsvp = self.events_dict.get(user_id).get(int(event_id)).get('rsvp')
                if clientEmail not in rsvp:
                    rsvp.append(clientEmail)
                    return {'success':True, 'message':rsvp}
                return {'success':False, 'message':"You already Reserved this event"}
            return {'success':False, 'message':"cannot find the event"}
        return {'success':False, 'message':"user does not exist"}
    def getRsvpForEvent(self, user_id, eventName):
        """
        gets all the rsvp for event
        """
        if user_id in self.events_dict:
            if eventName in self.events_dict.get(user_id):
                resp = self.events_dict.get(user_id).get(eventName).get('rsvp')
                return {'success':True, 'message':resp}
            return {'success':False, 'message':"cannot find the event"}
        return {'success':False, 'message':'user does not exist'}
    def generate_id(self, eventdata, proposed_id=0):
        if eventdata.get('creator'):
            if eventdata.get('creator') in self.events_dict:
                user_events = self.events_dict.get(eventdata.get('creator'))
                if proposed_id == 0:
                    proposed_id = str(eventdata.get('creator'))+str(len(user_events))
                if proposed_id in user_events:
                    self.generate_id(eventdata, proposed_id+1)
                return proposed_id
            self.events_dict.update({eventdata.get('creator'):{}})
            return int(str(eventdata.get('creator'))+"1")
        return None
    def get_event_id(self, event_name):
        for users in self.events_dict:
            for event_id, user_events in self.events_dict.get(users):
                if event_name == user_events.get('name'):
                    return event_id
        return None

