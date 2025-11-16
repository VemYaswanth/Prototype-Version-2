from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)

    # =============================
    # IMPORT MODELS (IMPORTANT)
    # =============================
    from app.models.user import User
    from app.models.query_log import QueryLog
    from app.models.anomaly import Anomaly
    from app.models.alert import Alert
    from app.models.blockchain_log import BlockchainLog
    from .routes.docker_manager import docker_bp

    # =============================
    # REGISTER ROUTES / BLUEPRINTS
    # =============================
    from app.routes.auth_routes import auth_bp
    from app.routes.log_routes import log_bp
    from app.routes.blockchain_routes import blockchain_bp
    from app.routes.ai_routes import ai_bp
    from app.routes.alerts_routes import alerts_bp
    from app.routes.metrics_routes import metrics_bp
    
    
    app.register_blueprint(docker_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(log_bp, url_prefix="/logs")
    app.register_blueprint(blockchain_bp, url_prefix="/blockchain")
    app.register_blueprint(ai_bp, url_prefix="/ai")
    app.register_blueprint(alerts_bp, url_prefix="/alerts")
    app.register_blueprint(metrics_bp, url_prefix="/metrics")

    app.url_map.strict_slashes = False
    return app