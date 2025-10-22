from datetime import datetime
from app import db

class Alert(db.Model):
    __tablename__ = 'alerts'

    alert_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(50), default="info")

    def __repr__(self):
        return f"<Alert {self.alert_id}: {self.message}>"