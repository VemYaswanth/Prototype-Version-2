from flask import Blueprint, jsonify, request
from app import db
from app.models import Anomaly, QueryLog

alerts_bp = Blueprint("alerts", __name__)

# GET /alerts/suspicious
@alerts_bp.route("/alerts/suspicious", methods=["GET"])
def suspicious_alerts():

    # Only anomalies flagged as anomalous
    alerts = Anomaly.query.filter_by(is_anomalous=True).all()

    result = []
    for a in alerts:
        log = QueryLog.query.filter_by(log_id=a.log_id).first()

        result.append({
            "alert_id": a.anomaly_id,
            "log_id": a.log_id,
            "score": a.anomaly_score,
            "model_version": a.model_version,
            "flagged_at": a.flagged_at,

            # Query log fields (OPTION A)
            "query_text": log.query_text if log else None,
            "operation": log.operation_type if log else None,
            "client_ip": log.client_ip if log else None,
            "executed_at": log.executed_at if log else None,
            "user_id": log.user_id if log else None,
        })

    return jsonify(result), 200


# POST /alerts/<id>/mark-safe
@alerts_bp.route("/alerts/<int:alert_id>/mark-safe", methods=["POST"])
def mark_safe(alert_id):
    alert = Anomaly.query.filter_by(anomaly_id=alert_id).first()
    if not alert:
        return jsonify({"error": "Alert not found"}), 404

    alert.is_anomalous = False
    db.session.commit()
    return jsonify({"message": "Alert marked safe"}), 200


# POST /alerts/<id>/resolve
@alerts_bp.route("/alerts/<int:alert_id>/resolve", methods=["POST"])
def resolve_alert(alert_id):
    alert = Anomaly.query.filter_by(anomaly_id=alert_id).first()
    if not alert:
        return jsonify({"error": "Alert not found"}), 404

    alert.is_anomalous = False
    db.session.commit()
    return jsonify({"message": "Alert resolved"}), 200