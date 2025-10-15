from flask import Blueprint, request, jsonify

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/score", methods=["POST"])
def score():
    # TODO: call anomaly detector service; return score + is_anomalous
    payload = request.get_json()
    return jsonify({"score": 0.02, "is_anomalous": False, "model_version": "v0"})
