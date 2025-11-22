import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)

def send_email(to, subject, body):
    if not SMTP_HOST or not SMTP_USERNAME or not SMTP_PASSWORD:
        print(f"[DEV MODE] Email to {to} | Subject: {subject} | Body: {body}")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to

    try:
        # If using SSL port (465), use SMTP_SSL
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=15)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
            if SMTP_USE_TLS:
                server.starttls()

        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[EMAIL] Sent to {to}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email to {to}: {e}")
