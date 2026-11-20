import unittest
from app import app, db
from models import Juego


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_juegos_creation(self):
        juego = Juego(nombre='Test', descripcion='Desc', precio=9.99)
        db.session.add(juego)
        db.session.commit()
        persisted = Juego.query.filter_by(nombre='Test').one()
        self.assertEqual(persisted.descripcion, 'Desc')

if __name__ == '__main__':
    unittest.main()