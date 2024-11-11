import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
      cls.client = app.test_client()

    def test_get_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"items": ["item1", "item2", "item3"]})

    def test_swagger_ui(self):
        response = self.client.get('/swagger')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_protected_with_invalid_token(self):
        invalid_token = "token incorreto"
        response = self.client.get('/protected', headers={'Authorization': f'Bearer {invalid_token}'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('The token is invalid', response.json['msg'])

if __name__ == '__main__':
    unittest.main()
