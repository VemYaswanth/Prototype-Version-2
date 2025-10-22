from datetime import datetime
from app import db

class QueryLog(db.Model):
    __tablename__ = 'query_logs'

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    query_text = db.Column(db.Text, nullable=False)
    operation_type = db.Column(db.String(50))
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_ip = db.Column(db.String(100))
    session_id = db.Column(db.String(100))
    blockchain_hash = db.Column(db.String(255))

    def __repr__(self):
        return f"<QueryLog {self.log_id}>"