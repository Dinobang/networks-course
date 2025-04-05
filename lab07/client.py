import socket
import time

HOST = '127.0.0.1'  
PORT = 12345        

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (HOST, PORT)


rtts = []

for i in range(10):

    lost_p = 0
    message = f"test {i+1}"
    print(f"Отправляю: {message}")
    
    client_socket.sendto(message.encode(), server_address)
    client_socket.settimeout(1)

    try:
        start = time.time()
        response, _ = client_socket.recvfrom(1024)
        end = time.time()

        time_rtt = end - start
        rtts.append(time_rtt)
        print(f"Получил: {response.decode()}, RTT = {time_rtt:.4f}")
    except socket.timeout:
        lost_p += 1
        print("Request timed out")
    
    if rtts:
            min_rtt = min(rtts) 
            avg_rtt = sum(rtts) / len(rtts)   
            max_rtt = max(rtts) 
            print(f"""Статистика по RTT: 
                  min/avg/max = {min_rtt:.6f}/{avg_rtt:.6f}/{max_rtt:.6f} с""")
    
    time.sleep(1) 

perc_lost = lost_p*100/10
print(f'Потеряно : {perc_lost:.0f}%')

client_socket.close()

