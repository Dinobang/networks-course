import socket 
import ipaddress

def get_ip_and_mask(): 
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        soc.connect(('196.0.0.0', 1))
        addr = soc.getsockname()[0]
        network = ipaddress.IPv4Network(addr)
    finally:
        soc.close()
    print(f'ip addr: {addr}, mask: {network.netmask}')
    return 
        
if __name__ == "__main__":
    get_ip_and_mask()


    
