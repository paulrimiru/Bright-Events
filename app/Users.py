"""
Module contains user model
"""
class Users(object):
    """
    class contains methods to manipulate users
    """
    def __init__(self):
        self.users_dict = {}
    def addUser(self, userData):
        """
        Adds user
        """
        EMAIL = userData.get('email')
        if EMAIL in self.users_dict:
            return {"success":False, 'message':"user with that email already exists"}
        else:
            self.users_dict.update({EMAIL:userData})
            return {"success":True, 'message':"user created successfully"}
    def getUsers(self):
        """
        gets all users
        """
        if self.users_dict:
            return {'success':True, "message":self.users_dict}
        else:
            return {'success':False, "message":'no users in the system yet'}
    def getUser(self, email):
        """
        gets specific user
        """
        if email in self.users_dict:
            return {'success':True, 'message':self.users_dict.get(email)}
        else:
            return {'success':False, 'message':"user not found"} 
    def deleteUser(self, email):
        """
        deletes user
        """
        if email in self.users_dict:
            self.users_dict.pop(email)
            return {'success':True, 'message':'user deleted'}
        else:
            return {'success':True, 'message':"user does not exist"}
    def updateUser(self, email, newUserData):
        """
        updates user details
        """
        if self.deleteUser(email).get('success'):
            if self.addUser(newUserData).get('success'):
                return {'success':True, 'message':'user details updated'}
            else:
                return {'success':False, 'message':self.addUser(newUserData).get('success').get('message')}
        else:
            return {'success':False, 'message':self.deleteUser(email).get('message')}
