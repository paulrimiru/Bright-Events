"""
Module contains controller tests
"""
import unittest
from app.Controller import Controller

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
            'creator':'user@bright.com',
            'rsvp':[]
        }
        self.event_data2 = {
            'name':'test event',
            'location':'Nairobi',
            'time':'5/6/2016',
            'rsvp':[]
        }
    def testRegisterUser(self):
        """
        tests user registration
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))
    def testLoginUser(self):
        """
        tests user login
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("message"))
    def testUserAddEvent(self):
        """
        tests ability for user to add events
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("message"))

        event = self.controller.addEvent(self.event_data)
        self.assertTrue(event.get('success'))
    def testAddEventWithoutCreator(self):
        """
        tests if an event can be added without a user
        """
        res = self.controller.addEvent(self.event_data2)
        self.assertFalse(res.get('success'))
    def testUpdateEvent(self):
        """
        tests ability for an event to be updated
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("message"))

        event = self.controller.addEvent(self.event_data)
        self.assertTrue(event.get('success'))
    def testRetriverAllEvents(self):
        """
        tests rettrieval of all events
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.addEvent(self.event_data)
        self.assertTrue(event.get('success'))

        eventsresp = self.controller.retrieveAllEvents()
        self.assertTrue(resp.get('success'))
        self.assertListEqual([self.event_data], eventsresp.get('message'))
    def testRetriveEventForCurrentUser(self):
        """
        tests retrieval of current users
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.addEvent(self.event_data)
        self.assertTrue(event.get('success'))

        eventsresp = self.controller.retrieveEvent('user@bright.com')
        self.assertTrue(eventsresp.get('success'))
        self.assertListEqual([self.event_data], eventsresp.get('message'))
    def testSaveRsvp(self):
        """
        tests addition of rsvp by users
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.addEvent(self.event_data)
        self.assertTrue(event.get('success'))

        rsvp = self.controller.addRsvp('user@bright.com', 'test event', 'myemail@bright.com')
        self.assertTrue(rsvp.get('success'))
        self.assertIn('myemail@bright.com', rsvp.get('message'))
    def testRetrieveRsvp(self):
        """
        tests rettrieval of rsvp of events
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.addEvent(self.event_data)
        self.assertTrue(event.get('success'))

        rsvp = self.controller.addRsvp('user@bright.com', 'test event', 'myemail@bright.com')
        self.assertTrue(rsvp.get('success'))
        self.assertIn('myemail@bright.com', rsvp.get('message'))

        retrive = self.controller.retriveRsvp('user@bright.com', 'test event')
        self.assertIn('myemail@bright.com', retrive.get('message'))
