from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from sqlalchemy import text

from config import Config
from models import db

jwt = JWTManager()

SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "EcoRoute Smart Waste API",
        "description": "API REST de planification intelligente de collecte des déchets",
        "version": "1.0.0",
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Entrez : Bearer <votre_token_JWT>",
        }
    },
    "security": [{"Bearer": []}],
}


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    Swagger(app, template=SWAGGER_TEMPLATE)

    @app.get("/api/health")
    def healthcheck():
        """
        Vérifier l'état de l'API et de la base MySQL
        ---
        tags:
          - Système
        responses:
          200:
            description: API et MySQL opérationnels
          500:
            description: Erreur de connexion MySQL
        """
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "ok", "bdd": "mysql connecte"}), 200
        except Exception as exc:
            return jsonify({"erreur": f"Erreur MySQL : {exc}"}), 500

    # Gestion uniforme des erreurs JWT
    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({"erreur": "Authentification requise"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"erreur": "Token invalide"}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"erreur": "Session expirée, veuillez vous reconnecter"}), 401

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)