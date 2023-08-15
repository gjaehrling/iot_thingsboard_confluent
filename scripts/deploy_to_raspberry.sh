#!/usr/bin/env bash

echo "Run deployment to Raspberry Pi"

host=$(jq .mqtt.host ../src/main/resources/config.json | sed 's/"//g')

echo "Deploying to $host"
echo "create directory ~/iot_thingsboard_telemetry"
ssh pi@"$host" "mkdir ~/iot_thingsboard_telemetry"
echo "copy files to $host"
scp -r ../* pi@"$host":~/iot_thingsboard_telemetry/

echo "subsrcibe to telemetry topic"
ssh pi@"$host" "mosquitto_sub -d -t telemetry > /dev/null &"

echo "start iot_thingsboard_telemetry and transfer to confluent"
ssh pi@"$host" "python3 ~/iot_thingsboard_telemetry/src/main/python/de/gbdmp/mqtt/telemetry/thingsboard_integration.py > /dev/null &"
ssh pi@"$host" "python3 ~/iot_thingsboard_telemetry/src/main/python/de/gbdmp/mqtt/telemetry/raspberry_telemetry.py > /dev/null &"