from flask import Blueprint, request
from flask_restful import Api, Resource, abort, marshal_with, fields

# Definir el Blueprint y la API de Flask-RESTful
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# Simulación de base de datos (puedes reemplazar esto con tu modelo SQLAlchemy existente)
juegos_db = [
    {"id": 1, "titulo": "The Legend of Zelda", "genero": "Aventura", "precio": 59.99},
    {"id": 2, "titulo": "Cyberpunk 2077", "genero": "RPG", "precio": 49.99}
]

# Esquema de serialización con Flask-RESTful
resource_fields = {
    'id': fields.Integer,
    'titulo': fields.String,
    'genero': fields.String,
    'precio': fields.Float
}

def abort_si_no_existe(juego_id):
    juego = next((j for j in juegos_db if j["id"] == juego_id), None)
    if not juego:
        abort(404, message=f"El juego con id {juego_id} no existe.")
    return juego

class JuegoList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        """Obtener la lista de todos los juegos"""
        return juegos_db, 200

    @marshal_with(resource_fields)
    def post(self):
        """Crear un juego nuevo"""
        if not request.is_json:
            abort(400, message="El payload debe ser JSON.")
        
        data = request.get_json()
        if not data or 'titulo' not in data or 'genero' not in data:
            abort(400, message="Faltan campos obligatorios (titulo, genero).")
            
        nuevo_id = max((j["id"] for j in juegos_db), default=0) + 1
        nuevo_juego = {
            "id": nuevo_id,
            "titulo": data["titulo"],
            "genero": data["genero"],
            "precio": float(data.get("precio", 0.0))
        }
        juegos_db.append(nuevo_juego)
        return nuevo_juego, 201

class JuegoResource(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        """Obtener un juego por su ID"""
        return abort_si_no_existe(id), 200

    @marshal_with(resource_fields)
    def put(self, id):
        """Modificar un juego existente"""
        juego = abort_si_no_existe(id)
        data = request.get_json()
        
        if not data:
            abort(400, message="No se proporcionaron datos para actualizar.")
            
        juego["titulo"] = data.get("titulo", juego["titulo"])
        juego["genero"] = data.get("genero", juego["genero"])
        juego["precio"] = float(data.get("precio", juego["precio"]))
        
        return juego, 200

    def delete(self, id):
        """Eliminar un juego"""
        juego = abort_si_no_existe(id)
        juegos_db.remove(juego)
        return '', 204

# Registrar los recursos en el API
api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')