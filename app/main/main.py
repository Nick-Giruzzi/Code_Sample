#!/usr/bin/env python3

import subprocess, io, datetime,socket
from flask import Blueprint, render_template_string, render_template, request, Response, current_app, send_file, make_response, flash, url_for, redirect, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
# Local Imports
from app.functions import recordLogin, send_email, delMFARecord
from app.models import Anonymous, User, MFACodes
from app.extensions import globals, db


main = Blueprint("main",__name__)       # add `, template_folder=f'templates', static_folder=f'static'` if url_prefix is enabled & blueprint unique templates and static folders are wanted

@main.route("/", methods=["GET","POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("auth.accounts"))
    return render_template("home.html")

@main.route("/login", methods=["GET","POST"])
def login():
    if request.method=='GET':
        if current_user.is_authenticated:
            return redirect(url_for("auth.accounts"))
        return render_template('login.html')
    else: 
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        # check if the user actually exists
        if (user == None) or (check_password_hash(user.password,password) == False):
            flash('Login incorrect')
            resp = make_response(render_template('login.html'),401)
            return resp
        # if the above check passes, then we know the user has the right credentials
        if user.mfa == True:
            ### THIS MAY NOT WORK -- alternative would be to write some tmp value to a globals attribute that can be called for reference in MFA function
            globals.mfa_login_user = user.id
            return redirect(url_for("main.mfa"))
        recordLogin(user, request.remote_addr)
        login_user(user, remember=True)
        session['last_activity'] = datetime.datetime.now(datetime.timezone.utc)
        resp = redirect(url_for('auth.accounts'))
        return resp


@main.route("/login/MFA",methods=['GET','POST'],defaults={'resend':None})
@main.route("/login/MFA/<path:resend>", methods=['GET','POST'])
def mfa(resend):
    # Check access & user
    if (request.referrer != f'{globals.fqdn}/login') and (request.referrer != f'{globals.fqdn}/login/MFA') and (request.referrer != f'{globals.fqdn}/login/MFA/resend') and (request.remote_addr != "10.7.7.100"):
        flash("Unauthorized access")
        return redirect(url_for('main.login'))
    elif globals.mfa_login_user == None:
        flash("Bad login. Please try again.")
        return redirect(url_for('main.login'))
    cur_user = User.query.filter_by(id=globals.mfa_login_user).first()

    if request.method == 'GET':
        reSend = True if resend == 'resend' else None
        status, resp = send_email(cur_user, login=True, resend=reSend)
        if status == False:
            flash(resp)
            globals.mfa_login_user = None
            return redirect(url_for('main.login'))
        elif resp != '':
            flash(resp)
        if request.remote_addr == '10.7.7.100':
            recordLogin(cur_user, '10.7.7.100')
        return render_template("mfa.html")
    else:
        data = request.form
        mfa_rec = MFACodes.query.filter_by(user_id=cur_user.id).first()
        if mfa_rec == None:
            flash("No MFA record found")
            globals.mfa_login_user = None
            return redirect(url_for('main.login'))
        if datetime.datetime.now() > mfa_rec.expires:
            delMFARecord(mfa_rec)
            globals.mfa_login_user = None
            flash("The code has expired. Please restart process to configure MFA.")
            return redirect(url_for('main.login'))
        elif data['code'] != mfa_rec.mfa_code:
            flash("Entered code did not match. Please try again.")
            return redirect(url_for("main.mfa"))
        delMFARecord(mfa_rec)
        globals.mfa_login_user = None
        #flash("Success!")
        recordLogin(cur_user, request.remote_addr)
        login_user(cur_user, remember=True)
        session['last_activity'] = datetime.datetime.now(datetime.timezone.utc)
        return redirect(url_for('auth.accounts'))