import os

import pymysql


def obtener_conexion():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ['DB_PASSWORD'],
        database=os.environ.get('DB_NAME', 'juegos'),
        port=int(os.environ.get('DB_PORT', '3306')),
    )