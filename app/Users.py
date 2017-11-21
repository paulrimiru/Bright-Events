class Users(object):
    def __init__(self):
        self.users_dict = {}
    def addUser(self, userData):
        userEmail = userData.get('email')
        if userEmail in self.users_dict:
            return "user with that email already exists"
        else:
            self.users_dict.update({userEmail:userData})
    def getUsers(self):
        return self.users_dict
    def getUser(self, email):
        if email in self.users_dict:
            return self.users_dict.get(email)
        else:
            return "user not found"
    def deleteUser(self, email):
        if email in self.users_dict:
            self.users_dict.pop(email)
        else:
            return "user does not exist"
    def updateUser(self, email, newUserData):
        self.deleteUser(email)
        self.addUser(newUserData)