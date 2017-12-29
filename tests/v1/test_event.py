"""
tests manipulation of the event model
"""
import unittest
from app.api_v1.models.events import Events

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
            'category':'private',
            'rsvp':[]
        }
        self.event_data2 = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':2,
            'category':'public',
            'rsvp':[]
        }

    def test_create_event(self):
        """
        class tests creation of events
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertIn(1, self.event.get_events().get('message'))

    def delete_event(self):
        self.test_create_event()
        self.assertTrue(self.event.delete_event(1, 11).get('success'))

    def test_get_user_events(self):
        """
        test retrival of users events
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))

        resp = self.event.get_user_events(1)
        self.assertTrue(resp.get('success'))
        self.assertEqual(1, len(resp.get('message')))
    def test_dublicate_event(self):
        """
        tests creation of duplicate users
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))

        self.assertFalse(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))
    def test_different_user_same_event_name(self):
        """
        tests creation of multiple events with same name by different users
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))
        self.assertTrue(self.event.create_event(self.event_data2).get('success'))
        self.assertEqual(2, len(self.event.get_events().get('message')))
    def test_get_single_event(self):
        """
        tests retrieval of a single event
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))

        resp = self.event.get_event(1, 11)
        self.assertTrue(resp.get('success'))
        self.assertIn('creator', resp.get("message"))
    def test_rsvp_event(self):
        """
        tests retrieval of rsvp of an event
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))
        resp = self.event.rsvp_event(1, 11, 'myemail@email.com')
        self.assertTrue(resp.get('success'))
        self.assertEqual(1, len(resp.get('message')))
    def test_delete_event(self):
        """
        tests deletion of events
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))
        resp = self.event.delete_event(1, 11)
        self.assertTrue(resp.get('success'))
        print(self.event.get_user_events(1).get('message'))
        self.assertEqual("No events for this user",
                         self.event.get_user_events(1).get('message'))
    def test_edit_event(self):
        """
        tests editing of an event
        """
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))

        event_data2 = {
            'name':'myevent',
            'location':'Nairobi',
            'time':'5/6/2016',
            'creator':1,
            'rsvp':[]
        }

        resp = self.event.edit_event(1, 11, event_data2)

        print(resp)
        self.assertTrue(resp.get('success'))
        self.assertEqual('myevent', resp.get('message').get('name'))
    def test_get_event_by_name(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))
        self.assertTrue(self.event.create_event(self.event_data2).get('success'))
        self.assertEqual(2, len(self.event.get_events().get('message')))

        self.assertEqual(2, len(self.event.get_event_by_name("test event").get('message')))
    def test_accept_rsvp(self):
        self.assertTrue(self.event.create_event(self.event_data).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))
        resp = self.event.rsvp_event(1, 11, 'myemail@email.com')
        self.assertTrue(resp.get('success'))
        self.assertEqual(1, len(resp.get('message')))
        self.assertTrue(self.event.confirm_rsvp(1, 11,'myemail@email.com').get('success'))
    def test_reject_rsvp(self):
        self.assertTrue(self.event.create_event(self.event_data2).get('success'))
        self.assertEqual(1, len(self.event.get_events().get('message')))
        resp = self.event.rsvp_event(2, 21, 'myemail@email.com')
        self.assertTrue(resp.get('success'))
        self.assertEqual(1, len(resp.get('message')))
        self.assertTrue(self.event.reject_rsvp(2, 21,'myemail@email.com').get('success'))
    