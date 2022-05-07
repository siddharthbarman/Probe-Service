# Using flask to make an api import necessary libraries and functions
from time import sleep
from flask import Flask, jsonify, request
from datetime import datetime
import sys
import os
import logging
from cmdline import CmdLine

# creating a Flask app
app = Flask(__name__)
started_at = datetime.now()
cmd = CmdLine("-", sys.argv)
version = "1"
 
@app.route('/health', methods=['GET'])
def health():
    return { "started_at": started_at, "uptime": (datetime.now() - started_at).total_seconds(), "version": version }

def getEnvVarValue(name, defaultValue):
    value = os.getenv(name);
    if value == None:
        value = defaultValue
    return value

def write_pid(file):
    with open(file, 'w') as f:
        f.write(str(os.getpid()))

# driver function
if __name__ == '__main__':
    for k, v in sorted(os.environ.items()):
        print(k, "=", v)

    pidFile = cmd.get_flag_value_default("PIDFILE", "probesvc.pid")
    logfile = cmd.get_flag_value_default("LOGFILE", "probesvc.log")    
    serverStartDelay = getEnvVarValue("SERVER_START_DELAY", 0)
    serverReadyDelay = getEnvVarValue("SERVER_READY_DELAY", 0)
    
    sleep(serverStartDelay)
    write_pid(pidFile)

    sleep(serverReadyDelay)
    logging.basicConfig(filename=logfile, filemode='w', level=logging.INFO)
    logging.info('Server started')

    app.run(host ='0.0.0.0', port = 5000, debug = False)
