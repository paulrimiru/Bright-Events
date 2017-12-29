"""Module containing the base test"""
import unittest

from app import DB, APP


class ApiTestCase(unittest.TestCase):
    """Class defining the base test"""
    def setUp(self):
        self.app = APP.test_client()
        DB.create_all()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()
    