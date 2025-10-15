from flask import Blueprint, request, jsonify
from app.models import QueryLog, BlockchainLog
from app import db

blockchain_bp = Blueprint("blockchain", __name__)

@blockchain_bp.route("/commit", methods=["POST"])
def commit_hash():
    data = request.get_json()
    # TODO: compute SHA-256, call Fabric SDK, return tx details
    ql = QueryLog.query.get(data.get("log_id"))
    if not ql:
        return jsonify({"error": "log not found"}), 404

    # Placeholder commit
    block_hash = "pending"
    tx_id = "pending"

    b = BlockchainLog(log_id=ql.log_id, block_hash=block_hash, transaction_id=tx_id)
    db.session.add(b)
    db.session.commit()

    return jsonify({"message": "queued", "blockchain_log_id": b.blockchain_id}), 202

@blockchain_bp.route("/verify/<int:log_id>", methods=["GET"])
def verify(log_id):
    # TODO: verify against Fabric network
    entry = BlockchainLog.query.filter_by(log_id=log_id).first()
    if not entry:
        return jsonify({"verified": False, "reason": "no record"}), 404
    return jsonify({"verified": entry.block_hash != "pending", "tx": entry.transaction_id})