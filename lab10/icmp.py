import os
import socket
import struct
import time
import select
import statistics

ICMP_ECHO_REQUEST = 8
ICMP_CODE = 0
TIMEOUT = 1  
COUNT = 10   

# из lab08
def calculate_checksum(data):
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return ~checksum & 0xFFFF


def create_packet(id, seq):
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, ICMP_CODE, 0, id, seq)
    data = struct.pack('d', time.time())
    body = header + data
    checksum = calculate_checksum(body)
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, ICMP_CODE, checksum, id, seq)
    new_body = header + data
    return new_body


def send_ping(sock, addr, id, seq):
    packet = create_packet(id, seq)
    sock.sendto(packet, (addr, 0))


def receive_ping(sock, id, seq):

    l_time = TIMEOUT
    while l_time > 0:
        s_time = time.time()
        ans = select.select([sock], [], [], l_time)
        spent = time.time() - s_time

        if not ans[0]:
            return None

        r_time = time.time()
        packet, _ = sock.recvfrom(1024)
        header = packet[20:28]
        pkt, _, _, recv_id, recv_seq = struct.unpack('!BBHHH', header)

        if pkt == 0 and recv_id == id and recv_seq == seq:
            sent = struct.unpack('d', packet[28:36])[0]
            return (r_time - sent) * 1000

        l_time -= spent
    return None


def ping(hostname):
    try:
        addr = socket.gethostbyname(hostname)
    except socket.gaierror:
        print(f"Не удалось найти хост")
        return

    print(f"\nPING {hostname} ({addr}) с {COUNT} icmp-пакетами:")

    id = os.getpid() & 0xFFFF
    delays = []
    lost = 0
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
        for seq in range(COUNT):
            send_ping(sock, addr, id, seq)
            delay = receive_ping(sock, id, seq)

            if delay is None:
                print("Пакет потерян(.")
                lost += 1
            else:
                print(f"Ответ получен! Время: {round(delay, 2)} мс")
                delays.append(delay)

            time.sleep(1)

    print("\n Статистики ")
    rec = COUNT - lost
    print(f"Отправлено: {COUNT}, Получено: {rec}, Потеряно: {lost}, Процент потерь: {lost * 100 // COUNT}%")
    

    if delays:
        if len(delays) > 1:
            stdev = statistics.stdev(delays) 
        else: 
            stdev = 0
        print(f"min = {round(min(delays), 2)}\n"
              f"mean = {round(statistics.mean(delays), 2)}\n"
              f"max = {round(max(delays), 2)}\n"
              f"stddev = {round(stdev, 2)} мс")


if __name__ == "__main__":
    host = input("Ожидаю адрес : ")
    ping(host)