class Categories(object):
    def __init__(self):
        self.categories_dict = {}
    def createCategory(self, category):
        if category.get('name') in self.categories_dict:
            return {'success':False,'message':"Category already exists"}
        else:
            self.categories_dict.update({category.get('name'): category})
            return {'success':True,'message':'Category created successfully'}
    def getAllCategories(self):
        return self.categories_dict
    def deleteCategory(self, name):
        if name in self.categories_dict:
            self.categories_dict.pop(name)
            return {'success':True,'message':'Category deleted successfully'}
        else:
            return {'success':False,'message':'Category not found'}
    def updateCategory(self, name, new_category):
        delresp = self.deleteCategory(name)
        if delresp.get('success'):
            resp = self.createCategory(new_category)
            if resp.get('success'):
                return {'success':True,'message':"Category update successfully"}
            else:
                return {'success':False,'message':resp.get('message')}
        else:
            return {'success':False,'message':delresp.get('message')} 
    def getSingleCategory(self, name):
        if name in self.categories_dict:
            
            return {'success':True,'message':self.categories_dict.get(name)}
        else:
            return {'success':True, 'message':"category not found"}