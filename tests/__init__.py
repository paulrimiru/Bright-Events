import unittest
from app.Events import Events
from app.Users import Users

class UserTest(unittest.TestCase):
    def setUp(self):
        self.user = Users()
        self.user_data = {
                'email': 'user@bright.com',
                'password': 'pass123',
                'username':'test user'
            }
        self.user_data2 = {
                'email': 'user2@bright.com',
                'password': 'pass123',
                'username':'test user'
            }

    def testusercreation(self):
        self.user.addUser(self.user_data)
        self.assertEqual(1, len(self.user.getUsers()))

    def testdublicateuseraddition(self):
        self.user.addUser(self.user_data)
        self.assertEqual(1, len(self.user.getUsers()))

        self.assertEqual("user with that email already exists", self.user.addUser(self.user_data))
    def testmultipleusercreation(self):
        self.user.addUser(self.user_data)
        self.assertEqual(1, len(self.user.getUsers()))

        self.user.addUser(self.user_data2)
        self.assertEqual(2, len(self.user.getUsers()))
    def testgetsingleuser(self):
        self.user.addUser(self.user_data)
        self.assertEqual(1, len(self.user.getUsers()))

        result = self.user.getUser("user@bright.com")
        self.assertIn("user@bright.com", result.get('email'))

    def testdeleteuser(self):
        self.user.addUser(self.user_data)
        self.assertEqual(1, len(self.user.getUsers()))

        self.user.addUser(self.user_data2)
        self.assertEqual(2, len(self.user.getUsers()))

        self.user.deleteUser("user@bright.com")
        self.assertEqual(1, len(self.user.getUsers()))

    def testupdateuser(self):
        self.user.addUser(self.user_data)
        self.assertEqual(1, len(self.user.getUsers()))
        
        new_data = {
            'email':'another@email.com',
            'password':'mypass123',
            'username':'user tested'
        }

        self.user.updateUser("user@bright.com", new_data)
        result = self.user.getUser("another@email.com")
        self.assertIn("user tested", result.get('username'))

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

        