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
    # Enable CORS to minimize issues from hitting self API
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


'''
######### Function to shut down all scheduled jobs when server is being shut down
def signal_handler(sig, frame):
    try:
        with app.app_context():
            #logout_user()
            scheduler.remove_all_jobs()
            session_list = LocalUser.query.all()
            for sesh in session_list:
                try:
                    loc_db.session.delete(sesh)
                    loc_db.session.commit()
                except:
                    continue
            print(f"{datetime.datetime.now().strftime('%m-%d-%Y, %H:%M')} -- Shutting Down Server.'")
        sys.exit(0)
    except Exception as e:
        print(f"Error shutting down:\n {e}")

        
######### Example function from C43 (art of the heist) of function configured to run when scheduler API was hit
@scheduler.authenticate
def authenticate(auth):
    with app.app_context():
        if (request.remote_addr == '10.7.7.7') or (request.remote_addr == "10.3.3.17"):
            return True
        if scheduler_auth(auth['username'],auth['password']):
            return True
        else:
            print(auth['username'], auth['password'])
            return False


######### Example function from C43 (art of the heist) of sending traffic to scheduler API
def monitor():
    req_auth = HTTPBasicAuth("gold","roger")
    url = "http://vault.merch.codes/scheduler/jobs"
    try:
        resp = requests.get(url,auth=req_auth)
    except Exception as e:
        print("cant make connection")
        return
    jobs = json.loads(resp.text)
    jobs_to_cancel = list()
    #print(json.dumps(output,indent=2))
    for job in jobs:
        if job['name'] == "restart_timer":
            continue
        ip_chk = check_ip(job['name'])
        if ip_chk == False:
            jobs_to_cancel.append(job['id'])

    if len(jobs_to_cancel) == 0:
        print("no bad jobs")
        return
    run_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    trigger_str = run_time.strftime("%Y-%m-%d %H:%M:%S")
    job_request = {
        "id": "remove_clients",
        "func":"app.functions:unauthorized_clients",
        "args":jobs_to_cancel,
        "trigger": "date",
        "run_date": trigger_str,
        "timezone": "America/New_York"
    }

    try:
        resp = requests.post('http://vault.merch.codes/scheduler/jobs', json=job_request, auth=req_auth)
    except Exception as e:
        print(str(e))
    else:
        print(resp.text)

'''