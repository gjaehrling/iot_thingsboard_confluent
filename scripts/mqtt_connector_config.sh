#!/usr/bin/env bash

# toDo: test the file

echo "configure mqtt connector:"
curl -X POST \
  http://localhost:8083/connectors \
  -H 'Content-Type: application/json' \
  -d '{ "name": "mqtt-source-connector",
    "config":
    {
      "connector.class":"io.confluent.connect.mqtt.MqttSourceConnector",
      "mqtt.server.uri": "tcp://192.168.4.104:1883",
      "kafka.topic": "raspberry_mqtt_telemetry",
      "mqtt.topics": "telemetry"
    }
}'