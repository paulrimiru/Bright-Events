import unittest
from app.Events import Events

class TestEvents(unittest.TestCase):
    def setUp(self):
        self.event = Events()
        self.event_data = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':'test@bright.com',
            'rsvp':[]
        }
        self.event_data2 = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':'test2@bright.com',
            'rsvp':[]
        }

    def testcreateEvent(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))

    def testGetUserEvents(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        resp = self.event.getUserEvents("test@bright.com")
        self.assertTrue(resp.get('success'))
        self.assertEqual(1, len(resp.get('message')))
    def testDublicateEvent(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        self.assertFalse(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))
    def testDifferentUserSameEventName(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))
        self.assertTrue(self.event.create_event(self.event_data2).get('success')) 
        self.assertEqual(2, len(self.event.getEvents().get('message')))
    def testGetSingleEvent(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        resp = self.event.getEvent('test@bright.com','test event')
        print(resp)
        self.assertTrue(resp.get('success'))
        self.assertIn('creator', resp.get("message"))
    def testRsvpEvent(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))
        resp = self.event.rsvpEvent('test@bright.com','test event', 'test2@bright.com')
        self.assertTrue(resp.get('success'))
        self.assertIn('test2@bright.com', resp.get('message'))
    def testDeleteEvent(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))
        resp = self.event.deleteEvent('test@bright.com', 'test event')
        self.assertTrue(resp.get('success')) 
        print(self.event.getUserEvents("test@bright.com").get('message'))
        self.assertEqual("No events for this user", self.event.getUserEvents("test@bright.com").get('message'))
    def testEditEvent(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success')) 
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        event_data2 = {
            'name':'myevent',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':'test@bright.com',
            'rsvp':[]
        }

        resp = self.event.editEvent('test@bright.com', 'test event', event_data2)

        print(resp)
        self.assertTrue(resp.get('success'))
        self.assertIn('myevent', self.event.getUserEvents("test@bright.com").get('message'))
