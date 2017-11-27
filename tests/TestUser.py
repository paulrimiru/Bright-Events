"""
tests manipulation of the user model
"""
import unittest
from app.Users import Users

class UserTest(unittest.TestCase):
    """
    contains tests for user model
    """
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
        """
        tests creation of users
        """
        self.assertTrue(self.user.addUser(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.getUsers().get('message')))

    def testdublicateuseraddition(self):
        """
        tests addition of dublicate users
        """
        self.assertTrue(self.user.addUser(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.getUsers().get('message')))

        self.assertFalse(self.user.addUser(self.user_data).get('success'))
    def testmultipleusercreation(self):
        """
        tests addition of multiple users
        """
        self.assertTrue(self.user.addUser(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.getUsers().get('message')))

        self.assertTrue(self.user.addUser(self.user_data2).get('success'))
        self.assertEqual(2, len(self.user.getUsers().get('message')))
    def testgetsingleuser(self):
        """
        tests ability to get one user
        """
        self.assertTrue(self.user.addUser(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.getUsers().get('message')))

        result = self.user.getUser("user@bright.com").get('message')
        self.assertIn("user@bright.com", result.get('email'))

    def testdeleteuser(self):
        """
        tests deletion of a user
        """
        self.assertTrue(self.user.addUser(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.getUsers().get('message')))

        self.assertTrue(self.user.addUser(self.user_data2).get('success'))
        self.assertEqual(2, len(self.user.getUsers().get('message')))

        self.assertTrue(self.user.deleteUser("user@bright.com").get('success'))
        self.assertEqual(1, len(self.user.getUsers().get('message')))

    def testupdateuser(self):
        """
        tests updating of a user details
        """
        self.assertTrue(self.user.addUser(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.getUsers().get('message')))
        new_data = {
            'email':'another@email.com',
            'password':'mypass123',
            'username':'user tested'
        }
        userresult = self.user.updateUser("user@bright.com", new_data)
        self.assertTrue(userresult.get('success'))
        result = self.user.getUser("another@email.com")
        self.assertIn("user tested", result.get('message').get('username'))
        