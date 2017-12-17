"""
Module contains controller tests
"""
import unittest
from app.api.Controller import Controller

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
        self.assertEqual('test user',loginres.get("payload").get('username'))
    def testUserAddEvent(self):
        """
        tests ability for user to add events
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertTrue(loginres.get("success"))

        event = self.controller.addEvent(self.event_data)
        self.assertEqual('test event',event.get('payload').get('name'))
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
        self.assertEqual('test user', loginres.get("payload").get('username'))

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
        self.assertListEqual([self.event_data], eventsresp.get('payload'))
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

        eventsresp = self.controller.retrieveEvent(1)
        self.assertTrue(eventsresp.get('success'))
        self.assertListEqual([self.event_data], eventsresp.get('payload'))
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

        rsvp = self.controller.addRsvp(1, 11, 'myemail@bright.com')
        self.assertTrue(rsvp.get('success'))
        self.assertDictEqual({'client': 'myemail@bright.com', 'accepted': False}, rsvp.get('payload')[0])
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

        rsvp = self.controller.addRsvp(1, 11, 'myemail@bright.com')
        self.assertTrue(rsvp.get('success'))
        self.assertDictEqual({'client': 'myemail@bright.com', 'accepted': False}, rsvp.get('payload')[0])

        retrive = self.controller.retriveRsvp(1, 11)
        self.assertListEqual([{'client': 'myemail@bright.com', 'accepted': False}], retrive.get('payload'))
    def testRetrieveEventsByName(self):
        """
        Tests to retrieve all events with specific names
        """
        resp = self.controller.registerUser(self.userData)
        self.assertTrue(resp.get('success'))

        loginres = self.controller.loginUser('user@bright.com', 'pass123')
        self.assertEqual('test user', loginres.get("payload").get('username'))

        event = self.controller.addEvent(self.event_data)
        self.assertTrue(event.get('success'))

        event = self.controller.addEvent(self.event_data3)
        self.assertTrue(event.get('success'))

        self.assertTrue(self.controller.retreiveEventsByName('test event').get('success'))
    def testAcceptRsvp(self):
        self.testSaveRsvp()
        resp = self.controller.acceptRsvp(1, 11, 'myemail@bright.com')
        self.assertTrue(resp.get('success'))
    def tstRejectRsvp(self):
        self.testAcceptRsvp()
        resp = self.controller.rejectRsvp(1, 11, 'myemail@bright.com')
        self.assertFalse(resp.get('payload')[0].get('rsvp')[0].get('accepted'))
