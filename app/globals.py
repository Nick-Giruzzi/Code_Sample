#!/usr/bin/env python3

import subprocess, os, logging, datetime
from flask_apscheduler import APScheduler
from datetime import timedelta, time

## Add entries below if you want variables to be able to be called, updated, and tracked throughout entire website

class Globals():
    def __init__(self):
        # Hostname
        self.fqdn = "https://steelbankofbravos.skills.hub"
        # File locations
        self.basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ssl_dir = f"{self.basedir}/app/ssl"
        # Data for MFA
        self.sender_email = "bravos@skills.hub"
        self.smtp_server = "box.skills.hub"
        self.smtp_port = 587
        self.smtp_password = "tartans@1"
        self.mfa_login_user = None
        # User account info
        self.user_email = "tlannister@skills.hub"
        self.auto_logout = datetime.timedelta(seconds=0,minutes=5)