#!/usr/bin/env python3

import logging
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
# local imports
from app.globals import Globals


#######
## This file contains all of the persistent objects that can be used throughout the sites execution
#######

# Create database object
db = SQLAlchemy()

# Instantiate globals object
globals = Globals()

# Instantiate scheduler object
scheduler = APScheduler()

# configure logging obj (default log level of INFO). 
# Requires systemd service to be named `webServer`
logging.basicConfig(format=f'Web-Server | %(message)s', level=logging.INFO)
logger = logging.getLogger("webServer")