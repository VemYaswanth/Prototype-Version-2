from datetime import datetime
from app import db

class Alert(db.Model):
    __tablename__ = 'alerts'

    alert_id = db.Column(db.Integer, primary_key=True)
    anomaly_id = db.Column(db.Integer, db.ForeignKey('anomalies.anomaly_id'))
    message = db.Column(db.Text)
    level = db.Column(db.String(50))
    alert_type = db.Column(db.String(100))
    confidence = db.Column(db.Float)  # 👈 This is the missing one
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Alert {self.alert_id}: {self.message}>"
