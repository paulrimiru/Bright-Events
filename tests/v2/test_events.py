import json
from tests.v2.test_base import ApiTestCase
class TestEvents(ApiTestCase):
    event_data = {
        'name':'test event',
        'location':'Nairobi',
        'time':'5/6/2016',
        'host':"1",
        'category':'1'
    }

    category_data = {
        'name':'private'
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
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        assert response.status_code == 200

        data = json.loads(response.data.decode('utf-8'))
        self.token = data.get('payload').get('token')

        response = self.app.post('/api/v2/events', data=self.event_data, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 201

        return data

    def test_createevent(self):
        self.create_event()
        
    def test_getevents(self):
        self.create_event()

        response = self.app.get('/api/v2/events', data=self.event_data)
        assert response.status_code == 200
    def test_get_while_empty(self):
        response = self.app.get('/api/v2/events', data=self.event_data, headers={'Authorization':' Bearer '+self.token})
        print(json.loads(response.data.decode('utf-8')))
        assert response.status_code == 401
    def test_get_single_event(self):
        data = self.create_event()

        event_id = data.get('payload').get('id')
        response = self.app.get('api/v2/events/'+event_id, data = self.event_data2, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 200
    def test_editevent(self):
        data = self.create_event()
        event_id = data.get('payload').get('id')

        response = self.app.put('api/v2/events/'+event_id, data = self.event_data2, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 200
    def test_edit_non_existent_event(self):
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        assert response.status_code == 200

        data = json.loads(response.data.decode('utf-8'))
        self.token = data.get('payload').get('token')

        response = self.app.put('api/v2/events/2', data = self.event_data2, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 401
    def test_delete_event(self):
        data = self.create_event()

        event_id = data.get('payload').get('id')
        response = self.app.delete('api/v2/events/'+event_id, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 200
    def test_delete_non_existent_event(self):
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        assert response.status_code == 200

        data = json.loads(response.data.decode('utf-8'))
        self.token = data.get('payload').get('token')

        response = self.app.delete('api/v2/events/2', headers={'Authorization':' Bearer '+self.token})
        print(response.status_code)
        assert response.status_code == 401
    def test_rsvp_event(self):
        data = self.create_event()
        event_id = data.get('payload').get('id')

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 201
    def test_rsvp_non_existent_event(self):
        response = self.app.post('api/v2/event/2/rsvp', data = self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 401
    
    def test_multiple_rsvp(self):
        data = self.create_event()
        event_id = data.get('payload').get('id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 201

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user2, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 201

    def test_dublicate_rsvp(self):
        data = self.create_event()
        event_id = data.get('payload').get('id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 201

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 401

    def test_retrieve_rsvp(self):
        data = self.create_event()
        event_id = data.get('payload').get('id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 201

        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user2, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 201

        response = self.app.get('/api/v2/event/'+event_id+'/rsvp', headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 200
    
    def test_accept_rsvp(self):
        
        data = self.create_event()
        event_id = data.get('payload').get('id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 201

        response = self.app.put('/api/v2/event/'+event_id+'/rsvp', data={'client_email':'test1@email.com','accept_status':True}, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 200
    def test_reject_rsvp(self):
        
        data = self.create_event()

        event_id = data.get('payload').get('id')
        
        response = self.app.post('/api/v2/event/'+event_id+'/rsvp', data=self.rsvp_user1, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 201

        response = self.app.put('/api/v2/event/'+event_id+'/rsvp', data={'client_email':'test1@email.com','accept_status':True}, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 200

        response = self.app.put('/api/v2/event/'+event_id+'/rsvp', data={'client_email':'test1@email.com','accept_status':False}, headers={'Authorization':' Bearer '+self.token})
        assert response.status_code == 200
    def test_filter_by_location(self):
        data = self.create_event()

        event_id = data.get('payload').get('id')

        response = self.app.get('/api/v2/events', data={'location':'Nairobi'})
        data = json.loads(response.data.decode('utf-8'))
        for event in data.get('payload').get('event_list'):
            self.assertEqual('Nairobi', event.get('location'))
    def test_filter_by_category(self):
        data = self.create_event()

        event_id = data.get('payload').get('id')

        response = self.app.get('/api/v2/events', data={'category':'1'})

        data = json.loads(response.data.decode('utf-8'))
        for event in data.get('payload').get('event_list'):
            self.assertEqual('1', event.get('category'))
    def test_filter_by_bot_category_and_location(self):
        data = self.create_event()

        event_id = data.get('payload').get('id')

        response = self.app.get('/api/v2/events', data={'category':'1', 'location':'Nairobi'})

        data = json.loads(response.data.decode('utf-8'))
        for event in data.get('payload').get('event_list'):
            self.assertEqual('1', event.get('category'))
            self.assertEqual('Nairobi', event.get('location'))
