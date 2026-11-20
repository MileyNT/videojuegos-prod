import json
import unittest

from flask import Flask
from api.routes import api_bp


class APITestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(api_bp)
        self.app = app
        self.client = app.test_client()

    def test_get_juegos(self):
        resp = self.client.get('/api/juegos')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()