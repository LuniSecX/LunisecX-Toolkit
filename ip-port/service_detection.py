import socket

# Port servis bilgilerini döndüren fonksiyon
def get_service_info(port):
    services = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        8080: "HTTP Proxy",
    }
    return services.get(port, "Bilinmeyen Servis")

def scan_with_service_info(ip, ports):
    for port in ports:
        scan_port(ip, port)

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = get_service_info(port)
            print(f"{ip} Port {port} açık, Servis: {service}")
        else:
            print(f"{ip} Port {port} kapalı.")
        sock.close()
    except socket.error:
        print(f"{ip} Port {port} hatalı.")
