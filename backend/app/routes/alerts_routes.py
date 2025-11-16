from flask import Blueprint, jsonify, request
from app import db
from app.models import Anomaly

alerts_bp = Blueprint("alerts", __name__)

# GET /alerts/suspicious
@alerts_bp.route("/alerts/suspicious", methods=["GET"])
def suspicious_alerts():
    alerts = Anomaly.query.filter_by(resolved=False).all()

    result = []
    for a in alerts:
        result.append({
            "alert_id": a.id,
            "description": a.description,
            "severity": a.severity,
            "source": a.source,
            "detected_at": a.detected_at,
            "resolved": a.resolved
        })

    return jsonify(result), 200


# POST /alerts/<id>/mark-safe
@alerts_bp.route("/alerts/<int:alert_id>/mark-safe", methods=["POST"])
def mark_safe(alert_id):
    alert = Anomaly.query.filter_by(id=alert_id).first()
    if not alert:
        return jsonify({"error": "Alert not found"}), 404

    alert.resolved = True
    db.session.commit()
    return jsonify({"message": "Alert marked safe"}), 200


# POST /alerts/<id>/resolve
@alerts_bp.route("/alerts/<int:alert_id>/resolve", methods=["POST"])
def resolve_alert(alert_id):
    alert = Anomaly.query.filter_by(id=alert_id).first()
    if not alert:
        return jsonify({"error": "Alert not found"}), 404

    alert.resolved = True
    db.session.commit()
    return jsonify({"message": "Alert resolved"}), 200
