import socket

HOST = '::1'  #IPv6 
PORT = 12345

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    connection, addr = server_socket.accept()
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            resp = data.decode().upper()
            connection.sendall(resp.encode())