# DDos Broker chạy trên mosquitto.

Được sử dụng trên Kali Linux Live 
## Step-by-step

### Attacker Side

1. Update your kali linux.


```sudo apt update```

2. Check your python version.

```python3 --version```

(I suggest lastest version for smooth and updated.

3. Download puho-mqtt (Yes! I recreate ddos script for IoT devices.)

```sudo apt install python-paho-mqtt```

4. Configurate and Enjoy.

### Broker monitor

Bạn có thể tham khảo cách cài broker ở ubuntu ver 24.04.

Có thể kiểm tra các thông tin dựa vào `top` hoặc `htop`: 

- Ở đây mình thích CLI nên sẽ dùng `top`:

```top -d 1 -p $(pgrep mosquitto)```

Trong đó: 
- `-d` : số giây cập nhật (hiện tại sẽ cập nhật 1s - Default sẽ là 3s).
- `-p` : PID.
- `pgrep mosquitto` : Tìm PID (process id) của tiến trình mosquitto và in ra số PID

- Ngoài ra bạn có thể xem CPU và MEM broker đang xài.


