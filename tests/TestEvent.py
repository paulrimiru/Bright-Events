"""
tests manipulation of the event model
"""
import unittest
from app.api.models.Events import Events

class TestEvents(unittest.TestCase):
    """
    class tests events manipulation
    """
    def setUp(self):
        self.event = Events()
        self.event_data = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':1,
            'rsvp':[]
        }
        self.event_data2 = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':2,
            'rsvp':[]
        }

    def testcreateEvent(self):
        """
        class tests creation of events
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertIn(1, self.event.getEvents().get('message'))

    def testGetUserEvents(self):
        """
        test retrival of users events
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        resp = self.event.getUserEvents(1)
        self.assertTrue(resp.get('success'))
        self.assertEqual(1, len(resp.get('message')))
    def testDublicateEvent(self):
        """
        tests creation of duplicate users
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        self.assertFalse(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))
    def testDifferentUserSameEventName(self):
        """
        tests creation of multiple events with same name by different users
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))
        self.assertTrue(self.event.create_event(self.event_data2).get('success'))
        self.assertEqual(2, len(self.event.getEvents().get('message')))
    def testGetSingleEvent(self):
        """
        tests retrieval of a single event
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        resp = self.event.getEvent(1, 11)
        print(resp)
        self.assertTrue(resp.get('success'))
        self.assertIn('creator', resp.get("message"))
    def testRsvpEvent(self):
        """
        tests retrieval of rsvp of an event
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))
        resp = self.event.rsvpEvent(1, 11, 'myemail@email.com')
        print(resp)
        self.assertTrue(resp.get('success'))
        self.assertIn('myemail@email.com', resp.get('message'))
    def testDeleteEvent(self):
        """
        tests deletion of events
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))
        resp = self.event.deleteEvent(1, 11)
        self.assertTrue(resp.get('success'))
        print(self.event.getUserEvents(1).get('message'))
        self.assertEqual("No events for this user",
                         self.event.getUserEvents(1).get('message'))
    def testEditEvent(self):
        """
        tests editing of an event
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))

        event_data2 = {
            'name':'myevent',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':1,
            'rsvp':[]
        }

        resp = self.event.editEvent(1, 11, event_data2)

        print(resp)
        self.assertTrue(resp.get('success'))
        self.assertEqual('myevent', resp.get('message').get('name'))
    def testgetEventsByName(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.getEvents().get('message')))
        self.assertTrue(self.event.create_event(self.event_data2).get('success'))
        self.assertEqual(2, len(self.event.getEvents().get('message')))

        self.assertEqual(2, len(self.event.getEventByName("test event").get('message')))
