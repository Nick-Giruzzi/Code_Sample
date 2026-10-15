#!/usr/bin/python3

import os, sys, smtplib, secrets, string, datetime, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash
# Local Import
from app.models import Logins, MFACodes, User
from app.extensions import globals, db

def send_email():
    
    mfaChars = string.ascii_letters + string.digits
    mfaCode = ''.join(secrets.choice(mfaChars) for i in range(8))

    # Create the email message
    message = MIMEMultipart()
    message["From"] = "bravos@skills.hub"
    message["To"] = "test@skills.hub"
    message["Subject"] = f"MFA Authentication Code"
    body = f"Your MFA authentication code is:\t\t{mfaCode}"
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP("box.skills.hub", 587) as server:
            server.starttls()  # Secure the connection
            server.login("bravos@skills.hub", "tartans@1")
            server.sendmail("bravos@skills.hub", "test@skills.hub", message.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    send_email()