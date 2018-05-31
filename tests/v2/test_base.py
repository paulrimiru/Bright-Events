"""Module containing the base test"""
import unittest

from app import APP, DB

class ApiTestCase(unittest.TestCase):
    """Class defining the base test"""
    def setUp(self):
        self.app = APP.test_client()
        with APP.app_context():
            DB.create_all()

    def tearDown(self):
        with APP.app_context():
            DB.session.remove()
            DB.drop_all()
    