# README #

Example connecting a Raspberry Pi 3B to TheThingsBoard and get some telemetry data in Confluent Platform 7.3

### Thingsboard Dashboard ###
Showing Raspberry Pi CPU temperature and load average on a Thingsboard dashboard.

![thingsboard_dashboard.png](docs%2Fthingsboard_dashboard.png)

### Confluent Control Center ###
Showing the messages in the topic raspberry_mqtt_telemetry

![confluent_telemetry_messages.png](docs%2Fconfluent_telemetry_messages.png)

### What is this repository for? ###

* Docker version of TheThingsBoard and Confluent platform 
* 1.0

### How do I get set up? ###

* to start the containers run docker-compose up -d
* TheThingsBoard is available under http://localhost:8080/
* Confluent Control Center under http://localhost:9021/clusters
* Get the IP address of the Raspberry and update config.json 
* Run the simple deploy_to_rasberry.sh to copy the code to the Raspberry Pi
* Run mqtt_connector_config.sh to start the connector (minimal example!)
* Check if mqtt processes are running on rapsberry
* Check if messages arrives in the raspberry_mqtt_telemetry topic

### Contribution guidelines ###

* ToDo: Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Gerd Jährling
* mail@gerd-jaehrling.de