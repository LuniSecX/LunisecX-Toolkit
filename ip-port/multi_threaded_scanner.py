import socket
import threading

# Port taraması
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
    except KeyboardInterrupt:
        print("\nTarama işlemi durduruldu.")
        exit(0)  # Programı güvenli bir şekilde sonlandır

# Multi-threading ile portları tarama
def thread_scan(ip, ports):
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Tarayıcıyı çalıştırmak için örnek kullanım
if __name__ == "__main__":
    target_ip = "127.0.0.1"  # Hedef IP adresi
    target_ports = [22, 80, 443, 8080]  # Hedef portlar
    thread_scan(target_ip, target_ports)  # Multi-threading ile tarama yap

