import unittest
import sys

sys.path.append('..')
from App import app

class FlaskTestClient(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.testing = True

    def test_valid_login(self):
        response = self.client.post('/login', data={
            'username': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 302) # code for redirect
        self.assertEqual(response.location, '/dashboard')
    
    def test_invalid_login_test(self):
        response = self.client.post('/login', data={
            'username': 'robert',
            'password': 'the_tank'
        })
        self.assertEqual(response.status_code, 200) # code for OK
        self.assertIn(b'invalid username or password', response.data)

    def test_login_directories(self):
        response = self.client.get('/ticket_view')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')

if __name__ == "__main__":
    unittest.main()

# in ~/homework-ticketing-system > python3 -m unittest discover tests -p '*_test.py'