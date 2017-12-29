"""
tests manipulation of the user model
"""
import unittest
from app.api_v1.models.users import Users

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

    def test_user_creation(self):
        """
        tests creation of users
        """
        self.assertTrue(self.user.add_user(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.get_users().get('message')))

    def test_dublicate_user_addition(self):
        """
        tests addition of dublicate users
        """
        self.assertTrue(self.user.add_user(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.get_users().get('message')))

        self.assertFalse(self.user.add_user(self.user_data).get('success'))
    def test_multiple_user_creation(self):
        """
        tests addition of multiple users
        """
        self.assertTrue(self.user.add_user(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.get_users().get('message')))

        self.assertTrue(self.user.add_user(self.user_data2).get('success'))
        self.assertEqual(2, len(self.user.get_users().get('message')))
    def test_get_single_user(self):
        """
        tests ability to get one user
        """
        self.assertTrue(self.user.add_user(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.get_users().get('message')))

        result = self.user.get_user("user@bright.com").get('message')
        self.assertIn("user@bright.com", result.get('email'))

    def test_delete_user(self):
        """
        tests deletion of a user
        """
        self.assertTrue(self.user.add_user(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.get_users().get('message')))

        self.assertTrue(self.user.add_user(self.user_data2).get('success'))
        self.assertEqual(2, len(self.user.get_users().get('message')))

        self.assertTrue(self.user.delete_user("user@bright.com").get('success'))
        self.assertEqual(1, len(self.user.get_users().get('message')))

    def test_update_user(self):
        """
        tests updating of a user details
        """
        self.assertTrue(self.user.add_user(self.user_data).get('success'))
        self.assertEqual(1, len(self.user.get_users().get('message')))
        new_data = {
            'email':'another@email.com',
            'password':'mypass123',
            'username':'user tested'
        }
        userresult = self.user.update_user("user@bright.com", new_data)
        self.assertTrue(userresult.get('success'))
        result = self.user.get_user("another@email.com")
        self.assertIn("user tested", result.get('message').get('username'))
        