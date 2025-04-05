import socket
import random

HOST = '127.0.0.1'  
PORT = 12345        

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("Сервер запущен, все хорошо")

while True:

    message, client_address = server_socket.recvfrom(1024)
    print(f"Получили: {client_address}: {message.decode()}")

    # Это у меня патеря пакета с вероятностью 20%
    if random.random() < 0.2:
        print("Пакет потерян.")
        continue

    mod_msg = message.upper()

    server_socket.sendto(mod_msg, client_address)
    print(f"Отправляем: {mod_msg.decode()}")
