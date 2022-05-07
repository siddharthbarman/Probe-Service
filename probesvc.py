# Using flask to make an api import necessary libraries and functions
from time import sleep
from flask import Flask, jsonify, request
from datetime import datetime
import sys
import os
import logging
import socket
from cmdline import CmdLine

def getEnvVarValue(name, defaultValue):
    value = os.getenv(name);
    if value == None:
        value = defaultValue
    return value

def write_pid(file):
    with open(file, 'w') as f:
        f.write(str(os.getpid()))

# creating a Flask app
app = Flask(__name__)
started_at = datetime.now()
cmd = CmdLine("-", sys.argv)
version = "1"

pidfile = cmd.get_flag_value_default("PIDFILE", "probesvc.pid")
logfile = cmd.get_flag_value_default("LOGFILE", "probesvc.log")    
server_start_delay = int(getEnvVarValue("SERVER_START_DELAY", 0))
server_ready_delay = int(getEnvVarValue("SERVER_READY_DELAY", 0))
server_port = int(getEnvVarValue("SERVER_PORT", 5000))
force_startup_failure = getEnvVarValue("FORCE_STARTUP_FAILURE", 0)
force_ready_failure = getEnvVarValue("FORCE_READY_FAILURE", 0)
fail_health_after_count = int(getEnvVarValue("FAIL_HEALTH_AFTER_COUNT", 0))
health_call_count = 0

@app.route('/health', methods=['GET'])
def health():
    global health_call_count
    health_call_count = health_call_count + 1
    if fail_health_after_count > 0 and health_call_count > fail_health_after_count:
        return { "health_call_count":  health_call_count }, 500        
    else:
        return { 
            "started_at": started_at, 
            "uptime": (datetime.now() - started_at).total_seconds(), 
            "version": version,
            "call_count": health_call_count
        }

# driver function
if __name__ == '__main__':
    for k, v in sorted(os.environ.items()):
        print(k, "=", v)

    print("IP:", socket.gethostbyname(socket.gethostname()))
    print("server_port:", server_port)
    print("pidFile:", pidfile)
    print("logfile:", logfile)
    print("server_start_delay:", server_start_delay)
    print("server_ready_delay:", server_ready_delay)
    print("force_startup_failure:", force_startup_failure)
    print("force_ready_failure:", force_ready_failure)
    print("fail_health_after_count:", fail_health_after_count)

    logging.basicConfig(level=logging.INFO, handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler(sys.stdout)
    ])

    sleep(server_start_delay)
    if force_startup_failure == "1":
        logging.critical("Forcing startup failure")
        exit()

    write_pid(pidfile)
    logging.info("PID file written")

    sleep(server_ready_delay)    
    if force_ready_failure == "1":
        logging.critical("Forcing ready failure")
        exit()
    logging.info('Server started')

    app.run(host ='0.0.0.0', port = server_port, debug = False)
