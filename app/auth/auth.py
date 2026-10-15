
import subprocess, io, datetime
from flask import Blueprint, render_template_string, render_template, request, Response, current_app, send_file, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.extensions import db
from app.functions import send_email, delMFARecord, updateUser
from app.models import Anonymous, User, Accounts, Transactions, Logins, MFACodes
import app.globals as globals

auth = Blueprint("auth",__name__) # add `, template_folder=f'templates', static_folder=f'static'` if url_prefix is enabled & blueprint unique templates and static folders are wanted

@auth.route("/accounts", methods=["GET","POST"],defaults={'acc_num':None})
@auth.route("/accounts/<path:acc_num>", methods=["GET","POST"])
@login_required
def accounts(acc_num):
    if acc_num == None:
        accs = Accounts.query.filter_by(user_id=current_user.id).all()
        return render_template("accounts.html",accs=accs)
    else:
        cur_acc = Accounts.query.filter_by(user_id=current_user.id, number=acc_num).first()
        if cur_acc == None:
            flash("Account not found.")
            return redirect(url_for("auth.accounts"))
        acc_trans = Transactions.query.filter_by(acc_id=cur_acc.id).all()
        return render_template("accounts.html",acc=cur_acc, trans=acc_trans)


@auth.route("/settings", methods=['GET','POST'],defaults={'setting':None})
@auth.route("/settings/<path:setting>", methods=['GET','POST'])
@login_required
def settings(setting):
    if request.method == 'GET':
        if setting == None:
            return render_template('settings.html', setting=None)
        elif (setting == 'MFA') or (setting == 'resend'):
            if (current_user.email == '') or (current_user.email == None):
                flash("Account needs a verified email in order to configure MFA.")
                return redirect(url_for('auth.settings'))
            ## Send email & wait for some code to be entered
            reSend = True if setting =='resend' else False
            status, resp = send_email(current_user, resend=reSend)
            if status == True:
                #flash(resp) if resp != '' else None
                return render_template('settings.html',setting='MFA')
            flash(resp)
            return redirect(url_for('auth.settings'))
        elif setting == 'disable':
            return render_template('settings.html', setting='disable')
        else:
            cur_logins = Logins.query.filter_by(user_id=current_user.id).all()
            return render_template('settings.html', setting='Login', logins=cur_logins)
    else:
        data = request.form
        if setting == None:
            update_resp = updateUser(current_user.id, data)
            if update_resp['failed'] == True:
                flash(update_resp['fail_msg'])
                return redirect(url_for('auth.settings'))
            msg = ""
            if update_resp['password'] != None:
                msg += f"<br>{update_resp['pwd_msg']}"
            if update_resp['email'] != None:
                msg += f"<br>{update_resp['email_msg']}"
            flash(msg)
            return redirect(url_for('auth.settings'))
        elif setting == 'disable':
            if data['disable'] == 'yes':
                try:
                    current_user.mfa = False
                    db.session.commit()
                except Exception as e:
                    flash(str(e))
                else:
                    flash("MFA Reset!")
            return redirect(url_for('auth.settings'))
        elif setting == 'MFA':
            try:
                mfa_rec = MFACodes.query.filter_by(user_id=current_user.id).one()
            except Exception as e:
                flash(str(e))
                #flash("No MFA record found in DB for veriying email.")
                return redirect(url_for('auth.settings'))
            if datetime.datetime.now() > mfa_rec.expires:
                delMFARecord(mfa_rec)
                flash("The code has expired. Please restart process to configure MFA.")
                return redirect(url_for('auth.settings'))
            elif data['code'] != mfa_rec.mfa_code:
                flash("Code did not match. Please try again.")
                return redirect(url_for('auth.settings',setting='MFA'))
            delMFARecord(mfa_rec)
            flash("Success! MFA configured.")
            cur_user = User.query.filter_by(id=current_user.id).first()
            cur_user.mfa = True
            db.session.commit()
            return redirect(url_for('auth.settings'))


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
