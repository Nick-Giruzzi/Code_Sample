#!/usr/bin/python3

import sys, os
from flask_cors import CORS
from apscheduler.events import EVENT_ALL, EVENT_JOB_MODIFIED ,EVENT_ALL_JOBS_REMOVED, EVENT_JOB_ERROR, EVENT_JOB_REMOVED, EVENT_SCHEDULER_PAUSED, EVENT_SCHEDULER_SHUTDOWN

# Local Imports
from app import create_app
from app.extensions import logger, globals, scheduler


app = create_app()
if __name__ == '__main__':
    if os.geteuid() != 0:
        logger.error("Program must be ran by root.")
        exit(1)
    CORS(app)

    ## Uncomment below code to implement scheduler w/ API
    #scheduler.init_app(app)
    #scheduler.add_listener(my_listener,EVENT_JOB_MODIFIED|EVENT_ALL_JOBS_REMOVED|EVENT_JOB_ERROR|EVENT_JOB_REMOVED|EVENT_SCHEDULER_PAUSED|EVENT_SCHEDULER_SHUTDOWN)
    #scheduler.add_job(id="",func=,trigger="",minute="",second="")
    ## Examples adding job
    #scheduler.add_job(id="send data",func=send_data,trigger="cron",minute="*",second="1")
    #scheduler.add_job(id="overload",func=overload,trigger="interval",seconds=pressure_timer)
    #scheduler.start()

    logger.info("Web Server starting up")
    app.run("0.0.0.0", port=443,ssl_context=(f'{globals.ssl_dir}/cert.pem',f'{globals.ssl_dir}/key.pem'), debug=False)

