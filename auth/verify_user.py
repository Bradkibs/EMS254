import secrets
from flask import url_for, jsonify
from flask_mail import Mail, Message
from os import getenv

def generate_verification_token():
    return secrets.token_urlsafe(16)


def send_verification_email(user_email, verification_token):
    subject = 'Verification Email for EMS254'
    mail = getenv('VERIFICATION_EMAIL')
    msg = Message(subject, sender=mail, recipients=[user_email])
    mail = Mail()
    verification_url = url_for('app_views.register', token=verification_token, _external=True)

    # Updated email body with a clear message.
    msg.body = f"Hello,\n\nPlease click the following link to verify your email address for EMS254:\n{verification_url}\n\nIf you didn't register for EMS254, you can safely ignore this email.\n\nBest regards,\nThe EMS254 Team"
    try:
        mail.send(msg)
        return jsonify({"Message": "Mail sent successfully", "status": 200})
    except Exception as e:
        return jsonify({"Mail sending Error": str(e), "status": 502})
