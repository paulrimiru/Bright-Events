import unittest
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
