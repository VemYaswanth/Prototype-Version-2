from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from app import db

# Models
from app.models import QueryLog, Alert, Anomaly

# AI / Blockchain Processor
from app.services.realtime_ai_monitor import process_new_query

log_bp = Blueprint("logs", __name__)


# ==========================================================
# GET ALL LOGS → GET /logs/
# ==========================================================
@log_bp.route("/", methods=["GET"])
@jwt_required(optional=True)
def list_logs():
    logs = (
        QueryLog.query.order_by(QueryLog.executed_at.desc())
        .limit(200)
        .all()
    )

    return jsonify([
        {
            "log_id": l.log_id,
            "user_id": l.user_id,
            "query_text": l.query_text,
            "operation_type": l.operation_type,
            "executed_at": l.executed_at.isoformat() if l.executed_at else None,
            "client_ip": l.client_ip,
            "session_id": str(l.session_id) if l.session_id else None,
            "blockchain_hash": l.blockchain_hash,
        }
        for l in logs
    ]), 200


# ==========================================================
# ADD LOG (AI + HASH) → POST /logs/add
# ==========================================================
@log_bp.route("/add", methods=["POST"])
@jwt_required(optional=True)
def add_log():
    data = request.get_json()

    executed_at = None
    if data.get("executed_at"):
        try:
            executed_at = datetime.fromisoformat(data["executed_at"])
        except:
            executed_at = datetime.utcnow()
    else:
        executed_at = datetime.utcnow()

    client_ip = data.get("client_ip") or request.remote_addr or "0.0.0.0"

    new_log = QueryLog(
        user_id=data.get("user_id"),
        query_text=data.get("query_text"),
        operation_type=data.get("operation_type"),
        client_ip=client_ip,
        executed_at=executed_at
    )

    db.session.add(new_log)
    db.session.commit()

    # Trigger AI anomaly detection + blockchain hashing
    try:
        process_new_query(
            log_id=new_log.log_id,
            query_text=new_log.query_text,
            operation_type=new_log.operation_type,
            executed_at=executed_at
        )
    except Exception as e:
        print(f"⚠️ AI/Hash processing failed: {e}")

    return jsonify({"log_id": new_log.log_id, "status": "processed"}), 201


# ==========================================================
# GET ALERTS → GET /logs/alerts
# ==========================================================
@log_bp.route("/alerts", methods=["GET"])
def list_alerts():
    alerts = (
        Alert.query.order_by(Alert.created_at.desc())
        .limit(200)
        .all()
    )

    return jsonify([
        {
            "alert_id": a.alert_id,
            "anomaly_id": a.anomaly_id,
            "alert_type": a.alert_type,
            "confidence": float(a.confidence or 0),
            "status": a.status,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ]), 200


# ==========================================================
# MARK ALERT SAFE → POST /logs/alerts/<id>/mark-safe
# ==========================================================
@log_bp.route("/alerts/<int:alert_id>/mark-safe", methods=["POST"])
def mark_alert_safe(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": "Alert not found"}), 404

    alert.status = "Safe"
    alert.resolved_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Alert marked as safe"}), 200


# ==========================================================
# RESOLVE ALERT → POST /logs/alerts/<id>/resolve
# ==========================================================
@log_bp.route("/alerts/<int:alert_id>/resolve", methods=["POST"])
def resolve_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": "Alert not found"}), 404

    alert.status = "Resolved"
    alert.resolved_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Alert resolved"}), 200