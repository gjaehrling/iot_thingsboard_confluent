#!/usr/bin/env python3

# general imports
import logging.handlers
import time
import os
from pathlib import Path
import json

# for logging:
import logging
from logging import config

# mqtt imports:
import paho.mqtt.client as mqtt

# constants:
ACCESS_TOKEN = "mey8q3gml5f81z2hfg7e"
THINGSBOARD_SERVER = '192.168.4.108'
THINGSBOARD_PORT = 1883

project_root = str(Path(__file__).parents[7])
logging_config = project_root + "/src/main/resources/logging.ini"

config.fileConfig(logging_config)


def get_data():
    try:
        cpu_usage = round(float(os.popen(
            '''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline().replace(
            '\n', '').replace(',', '.')), 2)
        ip_address = os.popen('''hostname -I''').readline().replace('\n', '').replace(',', '.')[:-1]
        mac_address = os.popen('''cat /sys/class/net/*/address''').readline().replace('\n', '').replace(',', '.')
        processes_count = os.popen('''ps -Al | grep -c bash''').readline().replace('\n', '').replace(',', '.')[:-1]
        swap_memory_usage = os.popen("free -m | grep Swap | awk '{print ($3/$2)*100}'").readline().replace('\n','').replace(',','.')[:-1]
        ram_usage = float(
            os.popen("free -m | grep Mem | awk '{print ($3/$2) * 100}'").readline().replace('\n', '').replace(',', '.')[
            :-1])
        st = os.statvfs('/')
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        boot_time = os.popen('uptime -p').read()[:-1]
        avg_load = (cpu_usage + ram_usage) / 2

        attributes = {
            'ip_address': ip_address,
            'macaddress': mac_address
        }
        telemetry = {
            'cpu_usage': cpu_usage,
            'processes_count': processes_count,
            'disk_usage': used,
            'RAM_usage': ram_usage,
            'swap_memory_usage': swap_memory_usage,
            'boot_time': boot_time,
            'avg_load': avg_load
        }

        logging.info("Attributes: {} Telemetry: {}".format(attributes,telemetry))
        return attributes, telemetry

    except Exception as e:
        logging.error("Error while getting data: " + str(e))


# request attribute callback
def sync_state(result, exception=None):
    global period
    if exception is not None:
        print("Exception: " + str(exception))
    else:
        period = result.get('shared', {'blinkingPeriod': 1.0})['blinkingPeriod']


def main():
    """main entry point, load and validate config and call generate"""

    project_root = str(Path(__file__).parents[7])
    config_path = project_root + "/" + "/src/main/resources/config.json"

    try:
        with open(config_path) as handle:
            config = json.load(handle)
            mqtt_config = config.get("mqtt", {})
            misc_config = config.get("misc", {})

            interval_ms = misc_config.get("interval_ms", 500)
            verbose = misc_config.get("verbose", False)

            host = mqtt_config.get("host", "localhost")
            port = mqtt_config.get("port", 1883)
            username = mqtt_config.get("username")
            password = mqtt_config.get("password")
            topic = mqtt_config.get("topic", "mqttgen")

    except IOError as error:
        logging.error("Error opening config file {} {}".format(config_path, error))
        exit(1)

    # sending telemetry without checking result:
    mqttc = mqtt.Client()

    if username:
        mqttc.username_pw_set(username, password)

    mqttc.connect(host, port)

    try:
        while True:
            attributes, telemetry = get_data()

            payload = json.dumps(telemetry)
            mqttc.publish(topic, payload)

            time.sleep(60)
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting...")
        exit(0)


if __name__ == '__main__':
    if ACCESS_TOKEN != "TEST_TOKEN":
        main()
    else:
        print("Please change the ACCESS_TOKEN variable to match your device access token and run script again.")
