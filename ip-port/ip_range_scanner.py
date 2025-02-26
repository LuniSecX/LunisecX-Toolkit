import socket

# IP aralığı tarama
def scan_ip_range(ports):
    ip_range = ["192.168.1.{}".format(i) for i in range(1, 256)]  # 192.168.1.1 - 192.168.1.255
    for ip in ip_range:
        for port in ports:
            scan_port(ip, port)

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"{ip} Port {port} açık.")
        else:
            print(f"{ip} Port {port} kapalı.")
        sock.close()
    except socket.error:
        print(f"{ip} Port {port} hatalı.")
