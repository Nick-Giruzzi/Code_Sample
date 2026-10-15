#!/usr/bin/python3

import os, sys
from flask import Flask, session
from flask_apscheduler.auth import HTTPBasicAuth

# local import
from app.extensions import globals

class Config:
    SECRET_KEY = 'THIS_IS_A_S3CRET'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(globals.basedir,'server.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'app.py'
    BASE_DIR = globals.basedir
    STATIC_FOLDER = f"{globals.basedir}/app/static"     
    TEMPLATES_FOLDER = f"{globals.basedir}/app/templates"
    # Settings that were referenced in C43 to configure scheduler API
    SCHEDULER_API_ENABLED = True
    SCHEDULER_AUTH =  HTTPBasicAuth()
    #SCHEDULER_API_PREFIX = "/scheduler"        ## Wasnt used but was present
    #SCHEDULER_ENDPOINT_PREFIX = "scheduler."   ## Wasnt used but was present
    #SCHEDULER_ALLOWED_HOSTS = ["*"]            ## Wasnt used but was present