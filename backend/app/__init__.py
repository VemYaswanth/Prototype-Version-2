from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Globals
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.log_routes import log_bp
    from app.routes.blockchain_routes import blockchain_bp
    from app.routes.ai_routes import ai_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(log_bp, url_prefix="/logs")
    app.register_blueprint(blockchain_bp, url_prefix="/blockchain")
    app.register_blueprint(ai_bp, url_prefix="/ai")

    return app