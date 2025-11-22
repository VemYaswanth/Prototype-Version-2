from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app.models.user import User
from app import db
from datetime import datetime, timedelta
import secrets
import os
import logging
import pyotp  # 🔐 Google Authenticator (TOTP)

auth_bp = Blueprint("auth", __name__)

FRONTEND_URL = os.getenv("FRONTEND_BASE_URL", "http://ssems.net:3000")


# ------------------------------- REGISTER -------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Generate TOTP secret for Google Auth
    mfa_secret = pyotp.random_base32()

    new_user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role="admin",
        mfa_enabled=True,
        mfa_secret=mfa_secret,
    )
    db.session.add(new_user)
    db.session.commit()

    logging.warning(f"[MFA SETUP] New user {email} TOTP secret: {mfa_secret}")

    return jsonify({"message": "User registered"}), 201


# ------------------------------- LOGIN STEP 1 -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # If MFA enabled, require Google Auth code
    if user.mfa_enabled:
        if not user.mfa_secret:
            user.mfa_secret = pyotp.random_base32()
            db.session.commit()
            logging.warning(f"[MFA SETUP] Generated TOTP secret for {email}: {user.mfa_secret}")

        totp = pyotp.TOTP(user.mfa_secret)
        logging.warning(f"[DEBUG] Current TOTP for {email}: {totp.now()}")

        mfa_token = create_access_token(
            identity=email,                     # identity MUST be a string
            additional_claims={"mfa": True},
            expires_delta=timedelta(minutes=10),
        )
        return jsonify({"mfa_required": True, "mfa_token": mfa_token})

    # If MFA disabled: return full access token
    access_token = create_access_token(
      identity=email,
      additional_claims={"role": user.role},
    )
    return jsonify({"mfa_required": False, "access_token": access_token})


# ------------------------------- VERIFY MFA (Google Auth) -------------------------------
@auth_bp.route("/mfa/verify", methods=["POST"])
@jwt_required()
def verify_mfa():
    email = get_jwt_identity()  # string
    claims = get_jwt()

    if not claims.get("mfa"):
        return jsonify({"error": "Invalid MFA token"}), 403

    user = User.query.filter_by(email=email).first()
    if not user or not user.mfa_secret:
        return jsonify({"error": "MFA not configured"}), 400

    data = request.get_json()
    code = data.get("code")

    totp = pyotp.TOTP(user.mfa_secret)
    if not totp.verify(code, valid_window=1):
        return jsonify({"error": "Invalid or expired code"}), 400

    # On success, issue full access token with role claim
    access_token = create_access_token(
        identity=email,
        additional_claims={"role": user.role},
    )

    return jsonify({"mfa_required": False, "access_token": access_token})


# ------------------------------- MFA SETUP (QR / secret) -------------------------------
@auth_bp.route("/mfa/setup", methods=["GET"])
@jwt_required()
def mfa_setup():
    """
    Returns secret + otpauth:// URL for Google Authenticator.
    Called from /mfa-setup page with a normal access token.
    """
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32()
        db.session.commit()
        logging.warning(f"[MFA SETUP] Generated TOTP secret for {email}: {user.mfa_secret}")

    totp = pyotp.TOTP(user.mfa_secret)
    otpauth_uri = totp.provisioning_uri(
        name=user.email,
        issuer_name="SSEMS Security",
    )

    return jsonify({
        "secret": user.mfa_secret,
        "otpauth_url": otpauth_uri,
    })


# ------------------------------- FORGOT PASSWORD -------------------------------
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    # Always respond success (no user enumeration)
    if not user:
        return jsonify({
            "message": "Reset link generated",
            "reset_url": None
        })

    token = secrets.token_urlsafe(32)
    user.reset_password_token = token
    user.reset_password_expires_at = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

    return jsonify({
        "message": "Reset link generated",
        "reset_url": reset_link
    })


# ------------------------------- RESET PASSWORD -------------------------------
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    user = User.query.filter_by(reset_password_token=token).first()

    if not user or user.reset_password_expires_at < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

    user.password_hash = generate_password_hash(
        new_password,
        method="pbkdf2:sha256",
        salt_length=16,
    )
    user.reset_password_token = None
    user.reset_password_expires_at = None
    db.session.commit()

    return jsonify({"message": "Password reset successful"})
