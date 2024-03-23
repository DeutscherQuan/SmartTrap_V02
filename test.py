import socket

ESP32_IP = '172.20.10.3'
ESP32_PORT = 1234              # Cổng kết nối ESP32

# Tạo socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Kết nối tới ESP32
    client_socket.connect((ESP32_IP, ESP32_PORT))
    print("Connected to ESP32.")

    # Gửi số "1" tới ESP32
    signal = '1'
    client_socket.sendall(signal.encode())
    print("Sent: 1")

finally:
    # Đóng kết nối và socket
    client_socket.close()

