import os
import secrets

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect

from models import User, db

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(
    __name__,
    template_folder=os.path.join(project_root, 'templates'),
    static_folder=os.path.join(project_root, 'static'),
)

database_url = os.environ.get('DATABASE_URL')
if os.environ.get('FLASK_ENV') == 'production' and not database_url:
    raise RuntimeError('DATABASE_URL must be set in production.')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url or (
    'mysql+pymysql://root@localhost:3306/juegos'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = os.environ.get('SECRET_KEY')
if os.environ.get('FLASK_ENV') == 'production' and not secret_key:
    raise RuntimeError('SECRET_KEY must be set in production.')
app.config['SECRET_KEY'] = secret_key or secrets.token_hex(32)

# Inicializamos la base de datos con la app
db.init_app(app)
CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Inicia sesión para acceder a esta página.'
login_manager.init_app(app)


@login_manager.user_loader
def cargar_usuario(user_id):
    if not user_id.isdecimal():
        return None
    return db.session.get(User, int(user_id))


# Importamos el controlador DESPUÉS de inicializar la app y db para evitar ciclos
import controlador_juegos
from .auth import auth

app.register_blueprint(auth, url_prefix='/auth')

@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    lista_juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=lista_juegos)

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    return redirect(url_for('juegos'))

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect(url_for('juegos'))

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect(url_for('juegos'))
