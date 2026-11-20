import unittest

from app import app, db


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_games_require_login(self):
        resp = self.client.get('/juegos')
        self.assertEqual(resp.status_code, 302)  # Redirect to login
        self.assertIn('/auth/login', resp.headers['Location'])

if __name__ == '__main__':
    unittest.main()
