from datetime import datetime
from app import db

class Anomaly(db.Model):
    __tablename__ = 'anomalies'

    anomaly_id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("query_logs.log_id"))
    anomaly_score = db.Column(db.Float, nullable=False)
    is_anomalous = db.Column(db.Boolean, nullable=False)
    model_version = db.Column(db.String(50))
    flagged_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Anomaly {self.anomaly_id} anomalous={self.is_anomalous}>"