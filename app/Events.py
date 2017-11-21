class Events(object):
    def __init__(self):
        self.events_dict = {}
    def create_event(self, eventData):
        name = eventData.get('name')
        creator = eventData.get('creator')

        if creator in self.events_dict:
            print(self.events_dict.get(creator))
            if name in self.events_dict.get(creator):
                return 'Duplicate event, choose a different name'
            else:
                user_events = self.events_dict.get(creator)
                user_events.update({name:eventData})
        else:
            new_event = {creator:{name:eventData}}
            self.events_dict.update(new_event)

    def getEvents(self):
        return self.events_dict;

    def getUserEvents(self, userEmail):
        return self.events_dict.get(userEmail)

    def deleteEvent(self, userEmail, eventName):
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                print(self.events_dict)
                self.events_dict.get(userEmail).pop(eventName)
                print(self.events_dict)
            else:
                return "Event not found"
        else:
            return "user does not have any events"
    def getEvent(self, userEmail, eventName):
        return self.getUserEvents(userEmail).get(eventName)
    def editEvent(self, userEmail, eventName, new_event):
        self.deleteEvent(userEmail, eventName)
        self.create_event(new_event)
    def rsvpEvent(self, userEmail, eventName, clientEmail):
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                rsvp = self.events_dict.get(userEmail).get(eventName).get('rsvp')
                rsvp.append(clientEmail)
            else:
                return "cannot find the event"
        else:
            return "user does not have any emails"
    def getRsvpForEvent(self, userEmail, eventName):
        if userEmail in self.events_dict:
            if eventName in self.events_dict.get(userEmail):
                return self.events_dict.get(userEmail).get(eventName).get('rsvp')
            else:
                return "cannot find the event"
        else:
            return "user does not have any emails"
