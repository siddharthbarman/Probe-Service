## Probe Service

### Description
A simple Python Flask service to demonstrate the use of start, 
readiness and liveliness probes of Kubernetes. 

### Configurations
The service can be controller using the following environment variables:

| Config Key   	        | Type   	    | Description   	                                                            |    
|---	                |---	        |---	                                                                        |
| SERVER_START_DELAY    | Env variable  | Seconds after which the service writes its pid to file                        |
| SERVER_READY_DELAY    | Env variable  | Seconds after which HTTP server starts   	                                    |
| FORCE_STARTUP_FAILURE | Env variable  | Forces the program to terminate after executing the start delay if set to 1   |
| FORCE_READY_FAILURE   | Env variable  | Forces the program to terminate after executing the ready delay if set to 1   |
| PIDFILE               | Command line  | Full path to the pid file   	                                                |
| LOGFILE               | Command line  | Full path to the log file                                                     |
### Endpoints
The service has just one endpoint '/health' which returns the following 
response:
```
{
    "call_count":2,
    "started_at":"Sat, 07 May 2022 15:58:14 GMT",
    "uptime":59.247903,
    "version":"1"
}
```
Calling the endpoint:
```
$ curl -XGET -i http://localhost:5000/health
```

### Docker
Build the container:
```
$ docker build -t siddharthbarman/probesvc:1.0 .
```

Run the container:
```
$ docker run -n prober -p 5000:5000 -it siddharthbarman/probesvc:1.0
```
Run with environment variables:
```
$ docker run -e FAIL_HEALTH_AFTER_COUNT=2 -it siddharthbarman/probesvc:1.0
```

Connect to the container:
```
$ docker container exec -it prober bash

```