import socket
import subprocess
import threading
import os
import platform

# Ping Taraması: IP aktif mi kontrol et
def ping(ip):
    print(f"\n{ip} IP adresi pingleniyor...")
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    
    if result.returncode == 0:
        print(f"{ip} aktif.")
        return True
    else:
        print(f"{ip} aktif değil.")
        return False

# Port taraması
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} açık.")
        else:
            print(f"Port {port} kapalı.")
        sock.close()
    except socket.error:
        pass

# Port tarama için multi-threading
def thread_scan(ip, ports):
    print("\nPort taraması başlatılıyor...")
    threads = []
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Traceroute
def traceroute(ip):
    print(f"\nTraceroute için {ip} başlatılıyor...")
    command = ["traceroute", ip] if platform.system().lower() != "windows" else ["tracert", ip]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        print("\nTraceroute sonuçları:")
        print(result.stdout.decode())
    else:
        print(f"Traceroute başarısız: {result.stderr.decode()}")

def display_menu():
    print("\n===============================")
    print("Gelişmiş IP Tarayıcı Araçları")
    print("===============================")
    print("1. Ping Tarama (IP aktif mi?)")
    print("2. Port Tarama (Belirli portları kontrol et)")
    print("3. Traceroute (IP'ye giden yolları göster)")
    print("4. Hepsini tara (Ping, Port ve Traceroute)")
    print("5. Çıkış")
    print("===============================")

def main():
    # Varsayılan IP adresi
    default_ip = "192.168.1.1"
    
    while True:
        display_menu()
        choice = input("\nBir seçenek girin: ")

        # Hedef IP adresi al
        if choice != "5":  # Çıkış işlemi dışında IP adresi al
            target_ip = input(f"Hedef IP adresini girin (Varsayılan: {default_ip}): ")
            target_ip = target_ip.strip() or default_ip  # Eğer boş bırakılırsa varsayılan IP kullanılır
        
        if choice == "1":
            ping(target_ip)
        elif choice == "2":
            try:
                ports = input("Hangi portları taramak istersiniz? (Örn: 22, 80, 443): ").split(",")
                ports = [int(port.strip()) for port in ports]  # Listeyi temizle ve sayılara dönüştür
                print(f"{target_ip} için port taraması başlatılıyor...")
                thread_scan(target_ip, ports)
            except ValueError:
                print("Geçersiz port numaraları girdiniz. Lütfen sadece sayılar girin.")
        elif choice == "3":
            traceroute(target_ip)
        elif choice == "4":
            if ping(target_ip):
                try:
                    ports = input("Hangi portları taramak istersiniz? (Örn: 22, 80, 443): ").split(",")
                    ports = [int(port.strip()) for port in ports]  # Listeyi temizle ve sayılara dönüştür
                    thread_scan(target_ip, ports)
                except ValueError:
                    print("Geçersiz port numaraları girdiniz. Lütfen sadece sayılar girin.")
                traceroute(target_ip)
        elif choice == "5":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçenek. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
