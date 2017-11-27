import unittest
from app.Categories import Categories

class TestCategory(unittest.TestCase):
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
        self.assertTrue(self.category.createCategory(self.category_data).get('success')) 
        self.assertEqual(1, len(self.category.getAllCategories()))
        
    def testCreationOfDublicateCategory(self):
        self.assertTrue(self.category.createCategory(self.category_data).get('success')) 
        self.assertEqual(1, len(self.category.getAllCategories()))

        resp = self.category.createCategory(self.category_data);
        self.assertFalse(resp.get('success'))
        self.assertEqual("Category already exists", resp.get('message'))
    def testCreationOfMultipleCategories(self):
        self.assertTrue(self.category.createCategory(self.category_data).get('success')) 
        self.assertEqual(1, len(self.category.getAllCategories()))

        self.assertTrue(self.category.createCategory(self.category_data2).get('success')) 
        self.assertEqual(2, len(self.category.getAllCategories()))
    def testDeleteCategory(self):
        self.assertTrue(self.category.createCategory(self.category_data).get('success')) 
        self.assertEqual(1, len(self.category.getAllCategories()))

        resp = self.category.deleteCategory("test category")
        self.assertTrue(resp.get('success'))
        self.assertEqual(0, len(self.category.getAllCategories()))
    def testUpdateCategory(self):
        self.assertTrue(self.category.createCategory(self.category_data).get('success')) 
        self.assertEqual(1, len(self.category.getAllCategories()))

        resp = self.category.updateCategory("test category", self.category_data2)
        self.assertTrue(resp)
        self.assertEqual("test category2", self.category.getSingleCategory('test category2').get('message').get('name'))
        