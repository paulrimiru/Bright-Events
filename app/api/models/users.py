"""
Module contains user model
"""
class Users(object):
    """
    class contains methods to manipulate users
    """
    def __init__(self):
        self.users_dict = {}
    def add_user(self, user_data):
        """
        Adds user
        """

        EMAIL = user_data.get('email')
        for key in self.users_dict:
            print(self.users_dict.get(key))
            if EMAIL == self.users_dict.get(key).get('email'):
                return {"success":False, 'message':"user with that email already exists"}
        user_id = self.generate_id()
        self.users_dict.update({user_id:user_data})
        return {"success":True, 'message':{'id':user_id, 'data':self.users_dict.get(user_id)}}
    def get_users(self):
        """
        gets all users
        """
        if self.users_dict:
            return {'success':True, "message":self.users_dict}
        return {'success':False, "message":'no users in the system yet'}
    def get_user(self, email):
        """
        gets specific user
        """
        user_id = self.get_user_id(email)
        if user_id:
            return {'success':True, 'message':self.users_dict.get(user_id), 'id': user_id}
        return {'success':False, 'message':"user not found"}
    def delete_user(self, email):
        """
        deletes user
        """
        user_id = self.get_user_id(email)
        if user_id:
            self.users_dict.pop(user_id)
            return {'success':True, 'message':'user deleted'}
        return {'success':False, 'message':"user does not exist"}
    def update_user(self, email, new_user_data):
        """
        updates user details
        """
        if self.delete_user(email).get('success'):
            if self.add_user(new_user_data).get('success'):
                return {'success':True, 'message':'user details updated'}
            return {'success':False,
                    'message':self.add_user(new_user_data).get('success').get('message')}
        return {'success':False, 'message':self.delete_user(email).get('message')}
    def generate_id(self, proposed_id = 0):
        if proposed_id == 0:
            proposed_id = len(self.users_dict)+1
        if proposed_id in self.users_dict:
            self.generate_id(proposed_id+1)
        return proposed_id
    def get_user_id(self, email):
        for user_id in self.users_dict:
            if email == self.users_dict.get(user_id).get('email'):
                return user_id
        return None  
