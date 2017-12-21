"""
Module contains controller tests
"""
import unittest
from app.api.controller import Controller

class TestController(unittest.TestCase):
    """
    Class contains tests for controller
    """
    def setUp(self):
        self.controller = Controller()

        self.userData = {
            'email': 'user@bright.com',
            'password': 'pass123',
            'username':'test user'
        }

        self.event_data = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'category':'private',
            'creator':1,
            'rsvp':[]
        }
        self.event_data3 = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'category':'public',
            'creator':2,
            'rsvp':[]
        }
        self.event_data2 = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'rsvp':[]
        }
    def test_register_user(self):
        """
        tests user registration
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))
    def test_login_user(self):
        """
        tests user login
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertEqual('test user',loginres.get("payload").get('username'))
    def test_resetpassword(self):
        self.test_login_user()
        self.controller.reset_password(self.userData.get('email'), 'pass123456')

        loginres = self.controller.login_user('user@bright.com', 'pass123456')
        self.assertEqual('test user',loginres.get("payload").get('username'))

    def test_user_add_events(self):
        """
        tests ability for user to add events
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.add_event(self.event_data)
        self.assertEqual('test event',event.get('payload').get('name'))

    def test_user_delete_event(self):
        self.test_user_add_events()
        delres = self.controller.delete_single_event(1, 11)
        self.assertTrue(delres.get('success'))
    def test_add_event_without_creator(self):
        """
        tests if an event can be added without a user
        """
        res = self.controller.add_event(self.event_data2)
        self.assertFalse(res.get('success'))
    def test_update_user_event(self):
        """
        tests ability for an event to be updated
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertEqual('test user', loginres.get("payload").get('username'))

        event = self.controller.add_event(self.event_data)
        self.assertTrue(event.get('success'))

        updateevent = self.controller.edit_event(1, 11, {
            'email': 'newemail@bright.com',
            'password': 'pass123',
            'creator': 1,
            'username':'test user me'
        })
        self.assertTrue(updateevent.get('success'))

    def test_retrieve_all_events(self):
        """
        tests rettrieval of all events
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.add_event(self.event_data)
        self.assertTrue(event.get('success'))

        eventsresp = self.controller.retrieve_all_event()
        self.assertTrue(resp.get('success'))
        self.assertListEqual([self.event_data], eventsresp.get('payload'))
    def test_retrieve_events_for_current_user(self):
        """
        tests retrieval of current users
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.add_event(self.event_data)
        self.assertTrue(event.get('success'))

        eventsresp = self.controller.retrieve_event(1)
        self.assertTrue(eventsresp.get('success'))
        self.assertListEqual([self.event_data], eventsresp.get('payload'))
    def test_save_rsvp(self):
        """
        tests addition of rsvp by users
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.add_event(self.event_data)
        self.assertTrue(event.get('success'))

        rsvp = self.controller.add_rsvp(1, 11, 'myemail@bright.com')
        self.assertTrue(rsvp.get('success'))
        self.assertDictEqual({'client': 'myemail@bright.com', 'accepted': False}, rsvp.get('payload')[0])
    def test_retrieve_rsvp(self):
        """
        tests rettrieval of rsvp of events
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.add_event(self.event_data)
        self.assertTrue(event.get('success'))

        rsvp = self.controller.add_rsvp(1, 11, 'myemail@bright.com')
        self.assertTrue(rsvp.get('success'))
        self.assertDictEqual({'client': 'myemail@bright.com', 'accepted': False}, rsvp.get('payload')[0])

        retrive = self.controller.retrieve_rsvp(1, 11)
        self.assertListEqual([{'client': 'myemail@bright.com', 'accepted': False}], retrive.get('payload'))
    def test_retrieve_event_by_name(self):
        """
        Tests to retrieve all events with specific names
        """
        resp = self.controller.regiser_user(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.login_user('user@bright.com', 'pass123')
        self.assertEqual('test user', loginres.get("payload").get('username'))

        event = self.controller.add_event(self.event_data)
        self.assertTrue(event.get('success'))

        event = self.controller.add_event(self.event_data3)
        self.assertTrue(event.get('success'))

        self.assertTrue(self.controller.retrive_events_by_name('test event').get('success'))
    def test_accept_rsvp(self):
        self.test_save_rsvp()
        resp = self.controller.accept_rsvp(1, 11, 'myemail@bright.com')
        self.assertTrue(resp.get('success'))
    def test_reject_rsvp(self):
        self.test_accept_rsvp()
        resp = self.controller.reject_rsvp(1, 11, 'myemail@bright.com')
        self.assertFalse(resp.get('payload').get('accepted'))
