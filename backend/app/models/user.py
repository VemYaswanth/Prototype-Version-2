from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔐 TOTP Google Authenticator secret
    mfa_secret = db.Column(db.String(32), nullable=True)

    # Legacy email MFA fields (still fine, but not used with Google Auth)
    mfa_enabled = db.Column(db.Boolean, default=True)
    mfa_code = db.Column(db.String(10), nullable=True)
    mfa_code_expires_at = db.Column(db.DateTime, nullable=True)

    # Reset Password Fields
    reset_password_token = db.Column(db.String(255), nullable=True)
    reset_password_expires_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
