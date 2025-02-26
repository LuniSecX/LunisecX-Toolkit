import socket
import threading
from colorama import Fore

# Port taraması
def scan_port(ip, port, protocol='tcp'):
    try:
        if protocol == 'tcp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol == 'udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print(f"Geçersiz protokol: {protocol}")
            return
        
        sock.settimeout(1)  # Timeout süresi 1 saniye
        result = sock.connect_ex((ip, port)) if protocol == 'tcp' else None  # TCP taraması
        if result == 0:
            print(f"{Fore.GREEN}{ip} Port {port} ({protocol.upper()}) açık.{Fore.RESET}")
        else:
            print(f"{Fore.RED}{ip} Port {port} ({protocol.upper()}) kapalı.{Fore.RESET}")
        sock.close()
    except socket.error:
        print(f"{Fore.YELLOW}{ip} Port {port} ({protocol.upper()}) hatalı.{Fore.RESET}")
    except KeyboardInterrupt:
        print("\nTarama işlemi durduruldu.")
        exit(0)  # Programı güvenli bir şekilde sonlandır

# Multi-threading ile portları tarama
def thread_scan(ip, ports, protocol='tcp'):
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port, protocol))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# IP Aralığı Tarama
def scan_ip_range(start_ip, end_ip, ports, protocol='tcp'):
    start_ip_parts = start_ip.split('.')
    end_ip_parts = end_ip.split('.')
    
    for i in range(int(start_ip_parts[3]), int(end_ip_parts[3]) + 1):
        ip = f"{start_ip_parts[0]}.{start_ip_parts[1]}.{start_ip_parts[2]}.{i}"
        print(f"{ip} için port taraması başlatılıyor...")
        thread_scan(ip, ports, protocol)

# Tarayıcıyı çalıştırmak için örnek kullanım
def main():
    try:
        target_ip = input("Hedef IP adresini girin: ")  # Kullanıcıdan IP al
        protocol = input("TCP mi yoksa UDP mi taramak istiyorsunuz? (tcp/udp): ").strip().lower()  # Protokol seçimi
        
        # Kullanıcıdan port aralığı al
        start_port = int(input("Başlangıç portunu girin: "))
        end_port = int(input("Bitiş portunu girin: "))
        target_ports = list(range(start_port, end_port + 1))  # Port aralığını oluştur
        
        scan_type = input("IP aralığı taraması yapmak ister misiniz? (evet/hayır): ").strip().lower()
        
        if scan_type == 'evet':
            start_ip = input("Başlangıç IP adresini girin: ")
            end_ip = input("Bitiş IP adresini girin: ")
            print(f"{start_ip} ile {end_ip} arasındaki IP'ler için tarama başlatılıyor...")
            scan_ip_range(start_ip, end_ip, target_ports, protocol)  # IP aralığı taraması
        else:
            print(f"{target_ip} için {protocol.upper()} protokolü ile port taraması başlatılıyor...")
            thread_scan(target_ip, target_ports, protocol)  # Multi-threading ile port taraması
        
    except KeyboardInterrupt:
        print("\nTarama işlemi durduruldu.")
        exit(0)

if __name__ == "__main__":
    main()
