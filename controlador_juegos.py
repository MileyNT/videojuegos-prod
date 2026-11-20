from decimal import Decimal
from models import Juego, db


def obtener_juegos():
    return Juego.query.all()


def obtener_juego_por_id(id):
    return db.session.get(Juego, id)


def insertar_juego(nombre, descripcion, precio):
    nuevo_juego = Juego(
        nombre=nombre,
        descripcion=descripcion,
        precio=Decimal(str(precio)),
    )
    db.session.add(nuevo_juego)
    db.session.commit()
    return nuevo_juego


def actualizar_juego(nombre, descripcion, precio, id):
    juego = db.session.get(Juego, id)
    if juego:
        juego.nombre = nombre
        juego.descripcion = descripcion
        juego.precio = Decimal(str(precio))
        db.session.commit()
    return juego


def eliminar_juego(id):
    juego = db.session.get(Juego, id)
    if juego:
        db.session.delete(juego)
        db.session.commit()
        return True
    return False