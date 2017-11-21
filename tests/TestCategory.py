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
        self.category.createCategory(self.category_data)
        self.assertEqual(1, len(self.category.getAllCategories()))
    def testCreationOfDublicateCategory(self):
        self.category.createCategory(self.category_data)
        self.assertEqual(1, len(self.category.getAllCategories()))

        self.assertEqual("Category already exists", self.category.createCategory(self.category_data))
    def testCreationOfMultipleCategories(self):
        self.category.createCategory(self.category_data)
        self.assertEqual(1, len(self.category.getAllCategories()))

        self.category.createCategory(self.category_data2)
        self.assertEqual(2, len(self.category.getAllCategories()))
    def testDeleteCategory(self):
        self.category.createCategory(self.category_data)
        self.assertEqual(1, len(self.category.getAllCategories()))

        self.category.deleteCategory("test category")
        self.assertEqual(0, len(self.category.getAllCategories()))
    def testUpdateCategory(self):
        self.category.createCategory(self.category_data)
        self.assertEqual(1, len(self.category.getAllCategories()))

        self.category.updateCategory("test category", self.category_data2)
        self.assertEqual("test category2", self.category.getSingleCategory('test category2').get('name'))
        