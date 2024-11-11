import unittest
from app import app
import werkzeug

if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"items": ["item1", "item2", "item3"]})

    def test_login(self):
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_protected_with_token(self):
        login_response = self.client.post('/login')
        token = login_response.get_json()['access_token']
        response = self.client.get('/protected', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Protected route"})

    def test_protected_no_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
