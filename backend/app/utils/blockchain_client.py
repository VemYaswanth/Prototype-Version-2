# backend/app/utils/blockchain_client.py
import hashlib
import json
import os

LEDGER_PATH = os.getenv("MOCK_LEDGER_PATH", "backend/mock_ledger.json")

def commit_log_to_blockchain(log_id: int, query_text: str):
    """Simulates committing a log to a blockchain."""
    payload = f"{log_id}:{query_text}"
    payload_hash = hashlib.sha256(payload.encode()).hexdigest()

    # Create a mock transaction
    tx_id = hashlib.md5(payload.encode()).hexdigest()[:12]

    ledger = {}
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r") as f:
            ledger = json.load(f)

    ledger[str(log_id)] = {"hash": payload_hash, "tx_id": tx_id}
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)

    return payload_hash, tx_id

def verify_log_from_blockchain(log_id: int):
    """Simulates verifying log against the local ledger."""
    if not os.path.exists(LEDGER_PATH):
        raise FileNotFoundError("No mock ledger found.")
    with open(LEDGER_PATH, "r") as f:
        ledger = json.load(f)
    record = ledger.get(str(log_id))
    if not record:
        raise ValueError(f"No blockchain record for log_id {log_id}")
    return record
