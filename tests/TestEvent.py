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
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))

    def testGetUserEvents(self):
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))

        self.assertEqual(1, len(self.event.getUserEvents("test@bright.com")))
    def testDublicateEvent(self):
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))

        self.assertEqual("Duplicate event, choose a different name",self.event.create_event(self.event_data))
    def testDifferentUserSameEventName(self):
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))
        self.event.create_event(self.event_data2)
        self.assertEqual(2, len(self.event.getEvents()))
    def testGetSingleEvent(self):
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))

        self.assertIn('creator', self.event.getEvent('test@bright.com','test event'))
    def testRsvpEvent(self):
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))

        self.event.rsvpEvent('test@bright.com','test event', 'test2@bright.com')
        self.assertIn('test2@bright.com', self.event.getRsvpForEvent('test@bright.com','test event'))
    def testDeleteEvent(self):
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))

        self.event.deleteEvent('test@bright.com', 'test event')
        self.assertEqual(0, len(self.event.getUserEvents("test@bright.com")))
    def testEditEvent(self):
        self.event.create_event(self.event_data)
        self.assertEqual(1, len(self.event.getEvents()))

        event_data2 = {
            'name':'myevent',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':'test@bright.com',
            'rsvp':[]
        }
        self.event.editEvent('test@bright.com', 'test user', event_data2)
        self.assertIn("myevent", self.event.getUserEvents("test@bright.com"))