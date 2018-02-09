"""Module contains events tests"""
import json
from tests.v2.test_base import ApiTestCase
class TestEvents(ApiTestCase):
    """Event tests class"""
    event_data = {
        'name':'test event',
        'location':'Nairobi',
        'time':'5/6/2016',
        'host':"1",
        'category':'1'
    }

    user_data = {
        'username': 'test user',
        'email': 'test@email.com',
        'password': '123456',
    }


    event_data2 = {
        'name':'test event',
        'location':'Nairobi',
        'time':'5/6/2016',
        'host':2,
        'category':'1'
    }

    rsvp_user1 = {'client_email':'test1@email.com'}
    rsvp_user2 = {'client_email':'test2@email.com'}
    token = "abc"

    def create_event(self):
        """create event"""
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertDictEqual({"id":1, "username":"test user", "email":"test@email.com"}, data)

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        data = json.loads(response.data.decode('utf-8'))
        self.token = data.get('payload').get('token')

        response = self.app.post('/api/v2/events', data=self.event_data, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        return data

    def test_createevent(self):
        """test creation of event"""
        self.create_event()
        
    def test_getevents(self):
        """test retrieval of events"""
        self.create_event()

        response = self.app.get('/api/v2/events', data=self.event_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    def test_get_while_empty(self):
        """test retrieveal of events from empty database"""
        response = self.app.get('/api/v2/events', data=self.event_data, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data.get('success'))
    def test_get_single_event(self):
        """test retrieve single event"""
        data = self.create_event()

        event_id = data.get('payload').get('event_id')
        response = self.app.get('api/v2/events/'+event_id, data = self.event_data2, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    def test_editevent(self):
        """test edit event"""
        data = self.create_event()
        event_id = data.get('payload').get('event_id')

        response = self.app.put('api/v2/events/'+event_id, data = self.event_data2, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    def test_edit_non_existent_event(self):
        """test edit of an event that doesnt exist"""
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertDictEqual({"id":1, "username":"test user", "email":"test@email.com"}, data)

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        data = json.loads(response.data.decode('utf-8'))
        self.token = data.get('payload').get('token')

        response = self.app.put('api/v2/events/2', data = self.event_data2, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data.get('success'))
    def test_delete_event(self):
        """test deletio fo events"""
        data = self.create_event()
        
        event_id = data.get('payload').get('event_id')
        response = self.app.delete('api/v2/events/'+event_id, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    def test_delete_non_existent_event(self):
        """test deletion of an event that doesnt exist"""
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertDictEqual({"id":1, "username":"test user", "email":"test@email.com"}, data)

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        data = json.loads(response.data.decode('utf-8'))
        self.token = data.get('payload').get('token')

        response = self.app.delete('api/v2/events/2', headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data.get('success'))
    def test_rsvp_event(self):
        """test reserving an event"""
        data = self.create_event()
        event_id = data.get('payload').get('event_id')

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    def test_rsvp_non_existent_event(self):
        """test reserving events that do not exist"""
        response = self.app.post('api/v2/event/2/rsvp', data = self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data.get('success'))
    
    def test_multiple_rsvp(self):
        """test multiple reservation of an event"""
        data = self.create_event()
        event_id = data.get('payload').get('event_id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user2, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

    def test_dublicate_rsvp(self):
        """test reserving same event multiple times"""
        data = self.create_event()
        event_id = data.get('payload').get('event_id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertFalse(data.get('success'))

    def test_retrieve_rsvp(self):
        """test retrieveing rsvp list for an event"""
        data = self.create_event()
        event_id = data.get('payload').get('event_id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user2, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        response = self.app.get('/api/v2/event/'+event_id+'/rsvp', headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    
    def test_accept_rsvp(self):
        """test accepting reservation of on private event"""
        data = self.create_event()
        event_id = data.get('payload').get('event_id')
        print(">>>>",data.get('payload'))
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        response = self.app.put('/api/v2/event/'+event_id+'/rsvp', data={'client_email':'test1@email.com','accept_status':True}, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    def test_reject_rsvp(self):
        """test rejecting reservation on any event"""
        data = self.create_event()

        event_id = data.get('payload').get('event_id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        response = self.app.put('/api/v2/event/'+event_id+'/rsvp', data={'client_email':'test1@email.com','accept_status':True}, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

        response = self.app.put('/api/v2/event/'+event_id+'/rsvp', data={'client_email':'test1@email.com','accept_status':False}, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))
    def test_filter_by_location(self):
        """test filtering retrieval of events by location"""
        data = self.create_event()

        event_id = data.get('payload').get('id')

        response = self.app.get('/api/v2/events/search', data={'q':'test event','location':'Nairobi'}, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        for event in data.get('payload').get('event_list'):
            self.assertEqual('Nairobi', event.get('location'))
    def test_filter_by_category(self):
        """test filtering retrieval of events by category"""
        data = self.create_event()
        event_id = data.get('payload').get('id')

        response = self.app.get('/api/v2/events/search', data={'q':'test event','category':'1'}, headers={'Authorization':' Bearer '+self.token})

        data = json.loads(response.data.decode('utf-8'))
        for event in data.get('payload').get('event_list'):
            self.assertEqual('1', event.get('category'))
    def test_filter_by_categoryandlocation(self):
        """test filtering retrieval of events by both category and location"""
        data = self.create_event()

        event_id = data.get('payload').get('id')

        response = self.app.get('/api/v2/events/search', data={'q':'test event','category':'1', 'location':'Nairobi'}, headers={'Authorization':' Bearer '+self.token})

        data = json.loads(response.data.decode('utf-8'))
        for event in data.get('payload').get('event_list'):
            self.assertEqual(1, len(data.get('payload').get('event_list')))
            self.assertEqual('1', event.get('category'))
            self.assertEqual('Nairobi', event.get('location'))
