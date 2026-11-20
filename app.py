import os
import secrets

from flask import Flask, jsonify, render_template, request
import werkzeug.exceptions
from models import db
from api.routes import api_bp  # Asegúrate de que exista api/routes.py con api_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "mysql+pymysql://root@localhost:3306/juegos"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

db.init_app(app)
app.register_blueprint(api_bp)


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_400(e):
    if request.path.startswith("/api"):
        return jsonify(code=400, name=e.name, description=e.description), 400
    return render_template("400.html"), 400


@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api"):
        return jsonify(code=404, name="Not Found", description=str(e)), 404
    return render_template("404.html"), 404


@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_405(e):
    if request.path.startswith("/api"):
        return jsonify(code=405, name=e.name, description=e.description), 405
    return render_template("405.html"), 405


@app.errorhandler(500)
def handle_500(e):
    if request.path.startswith("/api"):
        return jsonify(code=500, name="Internal Server Error", description=str(e)), 500
    return render_template("500.html"), 500


@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_api_error(e):
    if request.path.startswith("/api"):
        return jsonify(code=e.code, name=e.name, description=e.description), e.code
    return e


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)