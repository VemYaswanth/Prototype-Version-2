from datetime import datetime
from app import db

class BlockchainLog(db.Model):
    __tablename__ = 'blockchain_logs'

    id = db.Column(db.Integer, primary_key=True)
    transaction_hash = db.Column(db.String(255), nullable=False)
    block_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")

    def __repr__(self):
        return f"<BlockchainLog {self.transaction_hash}>"