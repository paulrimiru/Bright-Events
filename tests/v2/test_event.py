import json
from tests.v2.test_base import ApiTestCase
class TestEvents(ApiTestCase):
    event_data = {
        'name':'test event',
        'location':'Nairobi',
        'time':'5/6/2016',
        'host':"1",
        'category':'1',
        'rsvp':[]
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
        'category':'public',
        'rsvp':[]
    }
    def test_createevent(self):
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/categories', data=self.category_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/events', data=self.event_data)
        assert response.status_code == 201