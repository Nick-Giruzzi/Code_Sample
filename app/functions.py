#!/usr/bin/env python3

import os, sys, smtplib, secrets, string, datetime, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request

# Local Import
from app.models import Logins, MFACodes, User
from app.extensions import globals, db

def send_email(cur_user, login=False, resend=False):
    cur_mfa_rec = MFACodes.query.filter_by(user_id=cur_user.id).first()
    if (resend == False) and (login == False) and (cur_mfa_rec != None) and (datetime.datetime.now() < cur_mfa_rec.expires):
        return True, 'Using previously sent code'
    
    # Either resend past vaild code or generate new one
    if resend == True:
        mfaCode = cur_mfa_rec.mfa_code
    else:
        mfaChars = string.ascii_letters + string.digits
        mfaCode = ''.join(secrets.choice(mfaChars) for i in range(8))

    # Create the email message
    message = MIMEMultipart()
    message["From"] = globals.sender_email
    message["To"] = cur_user.email
    message["Subject"] = f"{cur_user.username} MFA Authentication Code"
    body = f"Your MFA authentication code is:\t\t{mfaCode}"
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP(globals.smtp_server, globals.smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(globals.sender_email, globals.smtp_password)
            server.sendmail(globals.sender_email, cur_user.email, message.as_string())
            #print("Email sent successfully")
    except Exception as e:
        msg = f"Error occurred trying to send email: {str(e)}"
        return False, msg
    # Create new record in MFACodes table for above code sent to record endtime
    # Check if record already exists, if it does, overwrite it.

    
    cur_time = datetime.datetime.now()
    expire_time = cur_time + datetime.timedelta(minutes=5)
    if cur_mfa_rec == None:
        try:
            new_mfa_record = MFACodes(user_id=cur_user.id, mfa_code=mfaCode, expires=expire_time)
            # with app.app_context():   # unsure if this will be needed
            db.session.add(new_mfa_record)
            db.session.commit()
        except Exception as e:
            msg = f"Error occurred trying to create new record in MFACodes table: {str(e)}"
            return False, msg
    else:
        try:
            cur_mfa_rec.mfa_code = mfaCode
            cur_mfa_rec.expires = expire_time
            db.session.commit()
        except Exception as e:
            msg = f"Error occurred trying to update record in MFACodes table: {str(e)}"
            return False, msg
    return True, ''
    

def delMFARecord(mfa_rec):
    try:
        db.session.delete(mfa_rec)
        db.session.commit()
    except Exception as e:
        print(f"Unable to delect MFA Record for user ID: {mfa_rec.user_id}")
    return


def recordLogin(cur_user, remote_ip):
    cur_time = datetime.datetime.now()
    status = "Successful Login"
    if (cur_user.mfa == True) and (remote_ip == '10.7.7.100'):
        remote_ip = "10.7.7.137"
        status = "Failed Login"
    new_login = Logins(user_id=1,originated=remote_ip, date=cur_time, session_type=status)
    try:
        db.session.add(new_login)
        db.session.commit()
    except Exception as e:
        print(f"Exception occurred trying to record logins: {str(e)}")
    return

def updateUser(uid, data):
    cur_user = User.query.filter_by(id=uid).first()
    track_updates = {
        "password": None,
        "pwd_msg": "",
        "email": None,
        "email_msg": "",
        "failed": False,
        "fail_msg": ""
    }

    if cur_user == None:
        track_updates['failed'] = True
        track_updates['fail_msg'] = "User not found with that ID"
        return track_updates

    if (data['old_password'] != None) and (data['old_password'] != ''):
        if (data['new_password'] != None) and (data['new_password'] != ''):
            if check_password_hash(cur_user.password,data['old_password']):
                cur_user.password = generate_password_hash(data['new_password'])
                track_updates['password'] = True
                track_updates['pwd_msg'] = "Password Updated!"
            else:
                track_updates['password'] = False
                track_updates['pwd_msg'] = "Incorrect password entered. Please try again."
        else:
            track_updates['password'] = False
            track_updates['pwd_msg'] = "New password missing. Please try again."

    if data['email'] != cur_user.email:
        if data['email'].lower() == 'none':
            cur_user.email = None
            track_updates['email'] = True
            track_updates['email_msg'] = "Email Reset."
            if cur_user.mfa == True:
                cur_user.mfa = False
                track_updates['email_msg'] += "<br>MFA Reset."
        elif '@' not in data['email']:
            track_updates['email'] = False
            track_updates['email_msg'] = "Invalid email entered."
        elif len(data['email'].split('@')[0]) == 0:
            track_updates['email'] = False
            track_updates['email_msg'] = "Invalid email entered."
        elif data['email'].split('@')[1].strip() != 'skills.hub':
            track_updates['email'] = False
            track_updates['email_msg'] = "Email must be in the 'skills.hub' domain."
        else:
            chk = send_confirmation(cur_user, data['email'])
            if chk:
                cur_user.email = data['email']
                track_updates['email'] = True
                track_updates['email_msg'] = "Email Updated."
                if cur_user.mfa == True:
                    cur_user.mfa = False
                    track_updates['email_msg'] += "<br>MFA Reset."
            else:
                track_updates['email'] = False
                track_updates['email_msg'] = "Unable to send email to that address. Please ensure it is correct and try again."
    db.session.commit()
    return track_updates

def send_confirmation(cur_user, new_email):
    # Create the email message
    message = MIMEMultipart()
    message["From"] = globals.sender_email
    message["To"] = new_email
    message["Subject"] = f"Email Confirmation"
    body = f"This address has been successfully linked to {cur_user.username}s Bank account!"
    message.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP(globals.smtp_server, globals.smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(globals.sender_email, globals.smtp_password)
            server.sendmail(globals.sender_email, new_email, message.as_string())
            #print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred trying to send email: {str(e)}")
        return False
    else:
        print(f"Confirmation email sent to {new_email}")
        return True


def get_data():
    if (request.remote_addr == '10.7.7.100'):
        userChk = User.query.filter_by(id=1).first()
        if userChk != None:
            return jsonify(userChk.to_dict())
    elif (request.remote_addr == "10.5.5.5"):
        respDict = dict()
        # get grade for if phishing attack succeeded
        logins = Logins.query.filter_by(user_id=1).all()
        if any(log.originated == "10.7.7.100" for log in logins):
            respDict['phish'] = True
        else:
            respDict['phish'] = False

        # Get grade for if MFA was configured correctly
        chk_user = User.query.filter_by(id=1).first()
        if chk_user.mfa == True:
            respDict['mfa'] = True
        else:
            respDict['mfa'] = False
        return jsonify(respDict)

    #    userData = dict()
    #    users = User.query.all()
    #    for ind, u in enumerate(users):
    #        userData[ind] = u.to_dict()
    #    return jsonify(userData)
    return jsonify({"Warning":"Unauthorized access"})

