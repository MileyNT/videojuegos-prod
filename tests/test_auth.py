import os
import unittest

os.environ['DATABASE_URL'] = 'sqlite://'
from app import app, db
from models import Juego, User


class AuthenticationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SQLALCHEMY_DATABASE_URI='sqlite://',
        )
        with app.app_context():
            db.create_all()

    def setUp(self):
        
        self.client = app.test_client()
        with app.app_context():
            db.session.query(User).delete()
            db.session.query(Juego).delete()
            db.session.commit()

    def test_game_routes_redirect_anonymous_users_to_login(self):
        cases = (
            ('get', '/juegos'),
            ('get', '/agregar_juego'),
            ('get', '/formulario_editar_juego/1'),
            ('post', '/guardar_juego'),
            ('post', '/actualizar_juego'),
            ('post', '/eliminar_juego'),
        )
        for method, path in cases:
            with self.subTest(path=path):
                response = getattr(self.client, method)(path)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.headers['Location'].startswith('/auth/login'))

    def test_registration_persists_user_and_authenticates_session(self):
        response = self.client.post(
            '/auth/register',
            data={
                'username': 'miley',
                'email': 'miley@example.com',
                'password': 'correct-horse-battery',
                'confirm_password': 'correct-horse-battery',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/juegos')
        with app.app_context():
            user = User.query.filter_by(username='miley').one()
            self.assertTrue(user.check_password('correct-horse-battery'))
            self.assertNotEqual(user.password_hash, 'correct-horse-battery')

        self.assertEqual(self.client.get('/juegos').status_code, 200)

    def test_login_and_logout_change_session_authentication(self):
        with app.app_context():
            user = User(username='miley', email='miley@example.com')
            user.set_password('correct-horse-battery')
            db.session.add(user)
            db.session.commit()

        response = self.client.post(
            '/auth/login',
            data={
                'username': 'miley',
                'password': 'correct-horse-battery',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get('/juegos').status_code, 200)

        response = self.client.post('/auth/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/auth/login')
        login_page = self.client.get('/auth/login')
        self.assertIn('Has cerrado sesión.', login_page.get_data(as_text=True))
        self.assertTrue(
            self.client.get('/juegos').headers['Location'].startswith('/auth/login')
        )

    def test_game_list_renders_when_games_exist(self):
        response = self.client.post(
            '/auth/register',
            data={
                'username': 'miley',
                'email': 'miley@example.com',
                'password': 'correct-horse-battery',
                'confirm_password': 'correct-horse-battery',
            },
        )
        self.assertEqual(response.status_code, 302)

        with app.app_context():
            db.session.add(
                Juego(
                    nombre='Test deployment',
                    descripcion='Production list check',
                    precio=19,
                )
            )
            db.session.commit()

        response = self.client.get('/juegos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test deployment', response.data)


if __name__ == '__main__':
    unittest.main()
