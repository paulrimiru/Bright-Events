"""
Module contains Events model
"""
class Events(object):
    """
    class contains methods that manipulates event models
    """
    def __init__(self):
        self.events_dict = {}
    def create_event(self, event_data, event_id=0):
        """
        creates events
        """
        event_id = self.generate_id(event_data, event_id)
        print("new event id", event_data.get('name')+str(event_id))
        if event_id:
            user_events = self.events_dict.get(event_data.get('creator'))            
            for events in user_events:
                if event_data.get('name') == user_events.get(events).get('name'):
                    return {'success':False,
                            'message':"Dublicate event, please change the event name"}
            event_data.update({'id':event_id})
            user_events.update({event_id:event_data})
            self.events_dict.update({event_data.get('creator'):user_events})
            print(self.events_dict)
            return {'success':True, 'message':{event_id:event_data}}
        else:
            return {'success':False, 'message': 'please provide the creator user id'}

    def get_events(self):
        """
        gets all evennts
        """
        return {'success':True, 'message':self.events_dict}
    def get_event_by_name(self, name):
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

    def get_user_events(self, user_id):
        """
        gets a users events
        """
        if user_id in self.events_dict:
            if self.events_dict.get(user_id):
                return {'success':True, 'message':self.events_dict.get(user_id)}
            return {'success':False, 'message':'No events for this user'}
        return {'success':False, 'message':'No user in events'}
    def delete_event(self, user_id, event_id):
        """
        deletes an event
        """
        if user_id in self.events_dict:
            if event_id in self.events_dict.get(user_id):
                self.events_dict.get(user_id).pop(event_id)
                return {'success':True, 'message':'Event deleted'}
            return {'success':False, 'message':'Event not found'}
        return {'success':False, 'message':'user does not have any events'}
    def get_event(self, user_id, event_id):
        """
        gets specific event
        """
        resp = self.get_user_events(user_id)
        print(resp)
        if resp.get('success'):
            if resp.get('message').get(event_id):
                return {'success':True, 'message':resp.get('message').get(event_id)}
            return {'success':False, 'message':'event does not exist'}
        return {'success':False, 'message':resp.get('message')}
    def edit_event(self, user_id, event_id, new_event):
        """
        edits specific event
        """
        resp = self.delete_event(user_id, event_id)
        if resp.get('success'):
            resp = self.create_event(new_event, event_id)
            if resp.get('success'):
                return {'success':True, 'message':new_event}
            return {'success':False, 'message':resp.get('message')}
        return {'success':False, 'message':resp.get('message')}

    def rsvp_event(self, user_id, event_id, client_email):
        """
        adds rsvpto event
        """
        if user_id in self.events_dict:
            if int(event_id) in self.events_dict.get(user_id):
                myevent = self.events_dict.get(user_id).get(int(event_id));
                rsvp_list = myevent.get('rsvp')
                for rsvp in rsvp_list:
                    if client_email == rsvp.get('client'):
                        return {'success':False, 'message':"You already Reserved this event"}
                if myevent.get('category') == 'private':
                    rsvp_list.append({'client':client_email, 'accepted':False})
                    return {'success':True, 'message':rsvp_list}
                rsvp_list.append({'client':client_email, 'accepted':True}) 
                return {'success':True, 'message':rsvp_list}
                
            return {'success':False, 'message':"cannot find the event"}
        return {'success':False, 'message':"user does not exist"}
    def get_rsvp_for_event(self, user_id, event_name):
        """
        gets all the rsvp for event
        """
        if user_id in self.events_dict:
            if event_name in self.events_dict.get(user_id):
                resp = self.events_dict.get(user_id).get(event_name).get('rsvp')
                return {'success':True, 'message':resp}
            return {'success':False, 'message':"cannot find the event"}
        return {'success':False, 'message':'user does not exist'}
    def generate_id(self, eventdata, proposed_id=0):
        if eventdata.get('creator'):
            if int(eventdata.get('creator')) in self.events_dict:
                user_events = self.events_dict.get(eventdata.get('creator'))
                if proposed_id == 0:
                    proposed_id = int(str(eventdata.get('creator'))+str(len(user_events)))
                if proposed_id not in user_events:
                    return proposed_id
                return self.generate_id(eventdata, proposed_id+1)
            self.events_dict.update({eventdata.get('creator'):{}})
            return int(str(eventdata.get('creator'))+"1")
        return None
    def get_event_id(self, event_name):
        for users in self.events_dict:
            for event_id, user_events in self.events_dict.get(users):
                if event_name == user_events.get('name'):
                    return event_id
        return None
    def confirm_rsvp(self, creatorId,eventId, clientemail):
        rsvpevent = self.get_rsvp_for_event(creatorId, eventId)
        if rsvpevent.get('success'):
            for rsvp in rsvpevent.get('message'):
                if rsvp.get('client') == clientemail:
                    rsvp['accepted'] = True
                    return {'success':True, 'message':rsvp}
                return {'success':False, 'message':'No Rsvp with that email found'}
        return rsvpevent
    
    def reject_rsvp(self, creatorId, eventId, clientemail):
        rsvpevent = self.get_rsvp_for_event(creatorId, eventId)
        if rsvpevent.get('success'):
            for rsvp in rsvpevent.get('message'):
                if rsvp.get('client') == clientemail:
                    print(rsvp)
                    if rsvp.get('accepted'):
                        rsvp['accepted'] = False
                        return {'success':True, 'message':rsvp}
                    return {'success':False, 'message':"The user rsvp has already been rejected"}
                return {'success':False, 'message':'No Rsvp with that email found'}
        return rsvpevent
