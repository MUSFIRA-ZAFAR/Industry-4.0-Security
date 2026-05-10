"""
Industry 4.0 Security Demo
IoT Sensor Simulator using MQTT
Author: Musfira
RQF Level 03

This script simulates industrial IoT sensors publishing
real-time data to a secured Mosquitto MQTT broker.
"""

import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# ── Configuration ──────────────────────────────────────────
BROKER   = "localhost"
PORT     = 1883
TOPIC    = "factory/sensor"
USERNAME = "mqttuser"
PASSWORD = "mqtt1234"
INTERVAL = 3  # seconds between readings
# ───────────────────────────────────────────────────────────

def on_connect(client, userdata, flags, rc):
    codes = {
        0: "Connected successfully",
        1: "Incorrect protocol version",
        2: "Invalid client ID",
        3: "Server unavailable",
        4: "Bad username or password",
        5: "Not authorized"
    }
    print(f"[MQTT] {codes.get(rc, 'Unknown error')}")
    if rc == 0:
        print(f"[MQTT] Broker: {BROKER}:{PORT}")
        print(f"[MQTT] Topic:  {TOPIC}")
        print(f"[MQTT] Auth:   Username/Password enabled")
        print("-" * 50)

def on_publish(client, userdata, mid):
    print(f"[MQTT] Message delivered — ID: {mid}")

def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected from broker")

def generate_sensor_data():
    """Simulate realistic industrial sensor readings"""
    return {
        "device"     : "sensor-01",
        "location"   : "Factory Floor A",
        "temperature": round(random.uniform(20.0, 65.0), 1),
        "pressure"   : round(random.uniform(88.0, 112.0), 1),
        "humidity"   : round(random.uniform(30.0, 80.0), 1),
        "status"     : "normal",
        "timestamp"  : datetime.now().isoformat()
    }

def main():
    print("=" * 50)
    print("  Industry 4.0 IoT Sensor Simulator")
    print("  Secure MQTT Communication Demo")
    print("=" * 50)

    # Setup client
    client = mqtt.Client(client_id="sensor-01")
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect    = on_connect
    client.on_publish    = on_publish
    client.on_disconnect = on_disconnect

    # Connect to broker
    print(f"\n[MQTT] Connecting to {BROKER}:{PORT}...")
    try:
        client.connect(BROKER, PORT, keepalive=60)
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return

    client.loop_start()
    time.sleep(1)

    print("\n[SIM] Starting sensor simulation...")
    print("[SIM] Press Ctrl+C to stop\n")

    try:
        while True:
            data = generate_sensor_data()
            payload = json.dumps(data)

            result = client.publish(TOPIC, payload, qos=1)

            print(f"[DATA] Temperature: {data['temperature']}°C | "
                  f"Pressure: {data['pressure']} kPa | "
                  f"Humidity: {data['humidity']}% | "
                  f"Status: {data['status']}")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\n\n[SIM] Stopping simulation...")
        client.loop_stop()
        client.disconnect()
        print("[SIM] Disconnected cleanly. Goodbye!")

if __name__ == "__main__":
    main()
