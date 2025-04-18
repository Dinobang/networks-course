import socket 

def find_ports(ip: str, start_port: int, end_port: int):
    ports = []
    
    for port in range(start_port, end_port+1):
        if port == 0:
            continue
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(0.5)
        res = soc.connect_ex((ip, port))

        if res != 0:
            ports.append(port)
        
        soc.close()
    return ports

if __name__ == "__main__":
    ip = input('ip: ')
    start_port = int(input('start_port: '))
    end_port = int(input('end_port: '))
    ports = find_ports(ip, start_port, end_port)
    print(f'Свободных портов: {len(ports)}')
    for p in ports: 
        print(p)