"""
Module contains Category module tests
"""
import unittest
from app.Categories import Categories

class TestCategory(unittest.TestCase):
    """
    contains category model tests
    """
    def setUp(self):
        self.category = Categories()
        self.category_data = {
            'name':'test category',
            'description':'test description'
        }
        self.category_data2 = {
            'name':'test category2',
            'description':'test description2'
        }
    def testCreationOfCategory(self):
        """
        tests creation of category
        """
        self.assertTrue(self.category.createcategory(self.category_data).get('success'))
        self.assertEqual(1, len(self.category.getallcategories()))
    def testCreationOfDublicateCategory(self):
        """
        Tests creation of buplicate category
        """
        self.assertTrue(self.category.createcategory(self.category_data).get('success'))
        self.assertEqual(1, len(self.category.getallcategories()))

        resp = self.category.createcategory(self.category_data)
        self.assertFalse(resp.get('success'))
        self.assertEqual("Category already exists", resp.get('message'))
    def testCreationOfMultipleCategories(self):
        """
        Tests creation of multiple categories
        """
        self.assertTrue(self.category.createcategory(self.category_data).get('success'))
        self.assertEqual(1, len(self.category.getallcategories()))

        self.assertTrue(self.category.createcategory(self.category_data2).get('success'))
        self.assertEqual(2, len(self.category.getallcategories()))
    def testDeleteCategory(self):
        """
        Tests deleteion of categories
        """
        self.assertTrue(self.category.createcategory(self.category_data).get('success')) 
        self.assertEqual(1, len(self.category.getallcategories()))

        resp = self.category.deletecategory("test category")
        self.assertTrue(resp.get('success'))
        self.assertEqual(0, len(self.category.getallcategories()))
    def testUpdateCategory(self):
        """
        Tests updating of a category
        """
        self.assertTrue(self.category.createcategory(self.category_data).get('success'))
        self.assertEqual(1, len(self.category.getallcategories()))

        resp = self.category.updatecategory("test category", self.category_data2)
        self.assertTrue(resp)
        self.assertEqual("test category2",
                         self.category.getsinglecategory('test category2')
                         .get('message').get('name'))
