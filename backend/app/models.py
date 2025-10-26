from app import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    mfa_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QueryLog(db.Model):
    __tablename__ = "query_logs"
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    query_text = db.Column(db.Text, nullable=False)
    operation_type = db.Column(db.String(10))
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_ip = db.Column(db.String(45))
    session_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))
    blockchain_hash = db.Column(db.Text)

class Anomaly(db.Model):
    __tablename__ = "anomalies"
    anomaly_id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("query_logs.log_id"))
    anomaly_score = db.Column(db.Float, nullable=False)
    is_anomalous = db.Column(db.Boolean, nullable=False)
    model_version = db.Column(db.String(50))
    flagged_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    __tablename__ = 'alerts'
    alert_id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(100))
    confidence = db.Column(db.Numeric(4, 2))        
    message = db.Column(db.Text)
    level = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())



class BlockchainLog(db.Model):
    __tablename__ = "blockchain_logs"
    blockchain_id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("query_logs.log_id"))
    block_hash = db.Column(db.Text, nullable=False)
    block_index = db.Column(db.Integer)
    transaction_id = db.Column(db.Text)
    committed_at = db.Column(db.DateTime, default=datetime.utcnow)

class ModelConfig(db.Model):
    __tablename__ = "model_config"
    config_id = db.Column(db.Integer, primary_key=True)
    param_name = db.Column(db.String(100))
    param_value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
