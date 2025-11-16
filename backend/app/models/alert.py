from datetime import datetime
from app import db

class Alert(db.Model):
    __tablename__ = 'alerts'

    alert_id = db.Column(db.Integer, primary_key=True)

    # FIXED foreign key → anomalies.anomaly_id
    anomaly_id = db.Column(
        db.Integer,
        db.ForeignKey('anomalies.anomaly_id'),
        nullable=True
    )

    alert_type = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    status = db.Column(db.String(20), default="Open")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    # Relationship back to anomaly
    anomaly = db.relationship("Anomaly", backref="alerts", lazy=True)

    def to_dict(self):
        return {
            "alert_id": self.alert_id,
            "anomaly_id": self.anomaly_id,
            "alert_type": self.alert_type,
            "confidence": self.confidence,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }