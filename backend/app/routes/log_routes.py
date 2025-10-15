from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import QueryLog, Alert
from app import db

log_bp = Blueprint("logs", __name__)

@log_bp.route("/", methods=["GET"])
@jwt_required(optional=True)
def list_logs():
    logs = QueryLog.query.order_by(QueryLog.executed_at.desc()).limit(100).all()
    return jsonify([
        {
            "id": l.log_id,
            "user_id": l.user_id,
            "query": l.query_text,
            "operation": l.operation_type,
            "time": l.executed_at.isoformat(),
            "hash": l.blockchain_hash,
        } for l in logs
    ])

@log_bp.route("/add", methods=["POST"])
@jwt_required(optional=True)
def add_log():
    data = request.get_json()
    log = QueryLog(
        user_id=data.get("user_id"),
        query_text=data.get("query_text"),
        operation_type=data.get("operation_type"),
        client_ip=request.remote_addr,
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({"id": log.log_id}), 201

@log_bp.route("/alerts", methods=["GET"])
@jwt_required(optional=True)
def list_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).limit(100).all()
    return jsonify([
        {
            "id": a.alert_id,
            "type": a.alert_type,
            "confidence": a.confidence,
            "status": a.status,
            "created_at": a.created_at.isoformat(),
        } for a in alerts
    ])
