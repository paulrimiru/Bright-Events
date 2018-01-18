from app import DB
from tests.v2.test_base import ApiTestCase

import json

class UserTest(ApiTestCase):
    """Class for user tests"""
    user_data = {
        'username': 'test user',
        'email': 'test@email.com',
        'password': '123456',
    }

    def test_registration(self):
        """Test user registration"""
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 201
        
    def test_duplicate_registration(self):
        """Test if duplicate emails registration is not successful"""
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 409

    def test_user_login(self):
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 201

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200
    def test_user_logout(self):
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/auth/login', data=self.user_data)
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200

        token = data.get('payload').get('token')
        response = self.app.post('api/v2/auth/logout', data=self.user_data, headers={'Authorization':' Bearer '+token})
        assert response.status_code == 200
    def test_password_reset(self):
        """test if users can successfully reset their passwords"""
        response = self.app.post('/api/v2/auth/register', data=self.user_data)
        assert response.status_code == 201

        response = self.app.post('/api/v2/auth/reset-password', data={
            'email': 'test@email.com'
        })
        assert response.status_code == 201

        data = json.loads(response.data.decode('utf-8'))

        pw_reset_code = data.get('payload').get('code')
        response = self.app.put('/api/v2/auth/reset-password', data={
            'code': "bad code",
            'password': 'abc123'
        })

        assert response.status_code == 401
        response = self.app.put('/api/v2/auth/reset-password', data={
            'code': pw_reset_code,
            'password': 'abc123'
        })
        assert response.status_code == 200

        response = self.app.post('/api/v2/auth/login', data={
            'email': 'test@email.com',
            'password': 'abc123'
        })
        assert response.status_code == 200
