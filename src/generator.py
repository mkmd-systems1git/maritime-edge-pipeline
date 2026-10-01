import asyncio
import json
import time
import random
import paho.mqtt.client as mqtt

# Point directly to the broker container inside our Docker network
BROKER = "mqtt-broker"
PORT = 1883

def generate_nmea_telemetry():
    # Simulating real-time ship GPS data strings
    lat = round(random.uniform(-4.0, -4.1), 4)  # Coordinates near Mombasa port
    lon = round(random.uniform(39.6, 39.7), 4)
    speed = round(random.uniform(12.0, 15.5), 1)  # Ship speed in knots
    return {
        "timestamp": int(time.time()),
        "lat": lat,
        "lon": lon,
        "speed_knots": speed,
        "engine_rpm": random.randint(720, 750)
    }

def main():
    client = mqtt.Client()
    
    # Wait for the broker container to finish booting up
    time.sleep(5)
    client.connect(BROKER, PORT, 60)
    print("🚀 Marine Instrumentation Simulator Started Streaming Data...")

    while True:
        data = generate_nmea_telemetry()
        # Publish payload string over the local ship network loop
        client.publish("ship/telemetry/raw", json.dumps(data))
        time.sleep(1)  # Emit a new sensor reading every single second

if __name__ == "__main__":
    main()
