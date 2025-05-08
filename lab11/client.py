import socket

HOST = '::1'  #IPv6 
PORT = 12345

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    while True: 
        mes = input('Введите сообщение: ')
        if mes.lower() == 'exit':
            exit
        else:
            client_socket.sendall(mes.encode())
        resp = client_socket.recv(1024)
        print("Ответное собщние:", resp.decode())