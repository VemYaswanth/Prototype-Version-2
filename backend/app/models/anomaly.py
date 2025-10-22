from datetime import datetime
from app import db

class Anomaly(db.Model):
    __tablename__ = 'anomalies'

    id = db.Column(db.Integer, primary_key=True)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default="medium")
    source = db.Column(db.String(100))
    resolved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Anomaly {self.id} - {self.severity}>"
