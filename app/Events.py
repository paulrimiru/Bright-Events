class Events(object):
    def __init__(self):
        self.events_dict = {}
    def create_event(self, eventData):
        name = eventData.get('name')
        if 'creator' in eventData:
            creator = eventData.get('creator')

            if creator in self.events_dict:
                if name in self.events_dict.get(creator):
                    return {'success':False, 'message':'Duplicate event, choose a different name'}
                else:
                    user_events = self.events_dict.get(creator)
                    user_events.update({name:eventData})
                    return {'success':True,'message':'Event succesfully added'}
            else:
                new_event = {creator:{name:eventData}}
                self.events_dict.update(new_event)
                return {'success':True,'message':'First Event added, Hurray!!'}
        else:
            return {'success':False, 'message':'no user field provided'}

    def getEvents(self):
        return {'success':True, 'message':self.events_dict}

    def getUserEvents(self, userEmail):
        if(self.events_dict.get(userEmail)):
            return {'success':True,'message':self.events_dict.get(userEmail)}
        else:
            return {'success':False, 'message':'No events for this user'}
    def deleteEvent(self, userEmail, eventName):
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                self.events_dict.get(userEmail).pop(eventName)
                return {'success':True,'message':'Event deleted'}
            else:
                return {'success':False,'message':'Event not found'}
        else:
            return {'success':False,'message':'user does not have any events'}
    def getEvent(self, userEmail, eventName):
        resp = self.getUserEvents(userEmail)
        if resp.get('success'):
            return {'success':True, 'message':resp.get('message')}
        else:
            return {'success':False, 'message':resp.get('message')}
    def editEvent(self, userEmail, eventName, new_event):
        resp = self.deleteEvent(userEmail, eventName)
        print(resp)
        if resp.get('success'):
            resp = self.create_event(new_event)
            if resp.get('success'):
                return {'success':True,'message':'Event successfully edited'}
            else:
                return {'success':False, 'message':resp.get('message')}
        else:
            return {'success':False, 'message':resp.get('message')}
                
        
    def rsvpEvent(self, userEmail, eventName, clientEmail):
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                rsvp = self.events_dict.get(userEmail).get(eventName).get('rsvp')
                rsvp.append(clientEmail)
                return {'success':True, 'message':rsvp}
            else:
                return {'success':False, 'message':"cannot find the event"}
        else:
            return {'success':False, 'message':"user does not exist"}
    def getRsvpForEvent(self, userEmail, eventName):
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                resp = self.events_dict.get(userEmail).get(eventName).get('rsvp')
                return {'success':True, 'message':resp}
            else:
                return {'success':False, 'message':"cannot find the event"} 
        else:
            return {'success':False, 'message':'user does not exist'}
