# Mini-sistema Flask

[![CI - Tests y Cobertura](https://github.com/MileyNT/U3---A3-/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/MileyNT/U3---A3-/actions/workflows/ci.yml)
[![Cobertura de Codecov](https://codecov.io/gh/MileyNT/U3---A3-/branch/main/graph/badge.svg)](https://codecov.io/gh/MileyNT/U3---A3-/branch/main)

## Pruebas

Instala las dependencias con `pip install -r requirements.txt` y ejecuta `pytest`.
La suite usa SQLite en memoria para no requerir un servidor de base de datos.

Para conectar la aplicación a MySQL, configura `DATABASE_URL` y `SECRET_KEY`
como variables de entorno. El helper legado de conexión directa usa
`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` y `DB_NAME`.
