"""
This module contails model for event categories
"""
class Categories(object):
    """
    This is a model for categories
    """
    def __init__(self):
        self.categories_dict = {}
    def createcategory(self, category):
        """
        method used to create categories
        """
        if category.get('name') in self.categories_dict:
            return {'success':False, 'message':"Category already exists"}
        self.categories_dict.update({category.get('name'): category})
        return {'success':True, 'message':'Category created successfully'}
    def getallcategories(self):
        """
        Method used to get all categories
        """
        return self.categories_dict
    def deletecategory(self, name):
        """
        Method used to delete a category
        """
        if name in self.categories_dict:
            self.categories_dict.pop(name)
            return {'success':True, 'message':'Category deleted successfully'}
        return {'success':False, 'message':'Category not found'}
    def updatecategory(self, name, new_category):
        """
        Method used to delete a category
        """
        delresp = self.deletecategory(name)
        if delresp.get('success'):
            resp = self.createcategory(new_category)
            if resp.get('success'):
                return {'success':True, 'message':"Category update successfully"}
            return {'success':False, 'message':resp.get('message')}
        return {'success':False, 'message':delresp.get('message')}
    def getsinglecategory(self, name):
        """
        method used to retrieve a single category
        """
        if name in self.categories_dict:
            return {'success':True, 'message':self.categories_dict.get(name)}
        return {'success':True, 'message':"category not found"}
        