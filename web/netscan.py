import socket
import threading
import sys

# Hedef IP veya domain
target = None

# Tarama yapılacak portlar
ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080, 8888, 5000, 9000, 10000, 5432]

# Port tarama fonksiyonu
def scan_port(target, port):
    try:
        # Soket oluşturma
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)  # Timeout süresi
        result = s.connect_ex((target, port))  # Bağlantı kurmaya çalış
        if result == 0:
            print(f"Port {port}/tcp açık ({socket.getservbyport(port)})")
        s.close()
    except socket.error:
        pass  # Hata oluşursa geç

# Yardım mesajı
def print_help():
    print("""
Netscan - Port Taraması Aracı

Kullanım:
    netscan.py [Hedef IP veya domain] [Seçenekler]

Hedef Belirtme:
    [Hedef]: IP adresi, domain adı veya ağ belirtebiliriz.
    Örnek: scanme.nmap.org, microsoft.com/24, 192.168.0.1

Port Seçenekleri:
    -p [port]: Belirli bir portu taramak için
    Örnek: -p 80

Diğer Seçenekler:
    -h, --help      Yardım mesajını görüntüler
    -v, --version   Sürüm bilgisini görüntüler

Örnekler:
    netscan.py example.com
    netscan.py example.com -p 80,443,8080
    netscan.py 192.168.1.1 -v

""")

# Version mesajı
def print_version():
    print("Netscan v1.0 - 2025")

# Çoklu portları aynı anda taramak için thread kullanma
def scan(target):
    print(f"\nTaramaya Başlandı: {target}")
    print("-" * 50)
    print(f"Netscan taraması: {target}")
    print("Portları tarıyor...\n")

    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("-" * 50)
    print("Tarama Tamamlandı.")

# Ana fonksiyon
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
    else:
        target = sys.argv[1]
        
        if target == '-h' or target == '--help':
            print_help()
        elif target == '-v' or target == '--version':
            print_version()
        else:
            scan(target)
