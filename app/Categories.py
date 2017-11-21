class Categories(object):
    def __init__(self):
        self.categories_dict = {}
    def createCategory(self, category):
        if category.get('name') in self.categories_dict:
            return "Category already exists"
        else:
            self.categories_dict.update({category.get('name'): category})
    def getAllCategories(self):
        return self.categories_dict
    def deleteCategory(self, name):
        if name in self.categories_dict:
            self.categories_dict.pop(name)
        else:
            return "category not found"
    def updateCategory(self, name, new_category):
        self.deleteCategory(name)
        self.createCategory(new_category)
    def getSingleCategory(self, name):
        if name in self.categories_dict:
            return self.categories_dict.get(name)
        else:
            return "category not found"