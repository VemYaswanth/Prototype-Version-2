from flask import Blueprint, request, jsonify
from app.models import QueryLog, BlockchainLog, db
from app.utils.blockchain_client import commit_log_to_blockchain, verify_log_from_blockchain

blockchain_bp = Blueprint("blockchain", __name__)

@blockchain_bp.route("/commit", methods=["POST"])
def commit_hash():
    data = request.get_json()
    log_id = data.get("log_id")
    ql = QueryLog.query.get(log_id)
    if not ql:
        return jsonify({"error": "Log not found"}), 404

    block_hash, tx_id = commit_log_to_blockchain(log_id, ql.query_text)

    b = BlockchainLog(
        log_id=log_id,
        block_hash=block_hash,
        transaction_id=tx_id,
        block_index=None  # can be fetched later
    )
    db.session.add(b)
    ql.blockchain_hash = block_hash
    db.session.commit()
    return jsonify({"block_hash": block_hash, "tx_id": tx_id}), 201

@blockchain_bp.route("/verify/<int:log_id>", methods=["GET"])
def verify(log_id):
    try:
        record = verify_log_from_blockchain(log_id)
        return jsonify({"verified": True, "record": record}), 200
    except Exception as e:
        return jsonify({"verified": False, "error": str(e)}), 500
