import unittest
import sys

sys.path.append('..')
from App import app

class FlaskTestClient(unittest.TestCase):
    def setup(self):
        self.client = app.test_client()
        app.testing = True

    def valid_login_test(self):
        response = self.client.get('/login', data={
            'username': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 302) # code for redirect
        self.assertEqual(response.location, 'http://127.0.0.1:5000/dashboard')
    
    def invalid_login_test(self):
        response = self.client.post('/login', data={
            'username': 'robert',
            'password': 'the_tank'
        })
        self.asserEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

if __name__ == "__main__":
    unittest.main()