import socket
import threading
import time
import sys

# Proxy dinleme portu
LISTENING_PORT = 8080

# Proxy dinleyicisi
def start_proxy():
    """Proxy sunucusunu başlatır, belirtilen portu dinler ve bağlantı alır."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', LISTENING_PORT))
    server_socket.listen(5)
    print(f"Proxy dinleniyor: {LISTENING_PORT} portunda...")

    while True:
        # Bağlantıları kabul etme
        client_socket, client_address = server_socket.accept()
        print(f"Bağlantı alındı: {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# İstemci isteği işleyicisi
def handle_client(client_socket):
    """İstemciden gelen isteği alır, hedef sunucuya iletir ve yanıtı geri gönderir."""
    request = client_socket.recv(1024)
    print(f"İstemci isteği alındı: {request[:50]}")

    # Hedef sunucuya bağlantı
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect(('example.com', 80))  # Burada hedef siteyi değiştirin
    target_socket.send(request)

    response = target_socket.recv(4096)
    print(f"Sunucudan alınan yanıt: {response[:50]}")

    # Burada cevaba enjekte etmek istediğiniz içerikleri ekleyebilirsiniz
    # Örnek: HTML içerisindeki </body> etiketini değiştirmek
    try:
        response = response.decode('utf-8').replace("</body>", "<h1>Enjekte Edilmiş İçerik</h1></body>").encode('utf-8')
    except UnicodeDecodeError:
        print("Yanıt kod çözme hatası!")

    # İstemciye yanıt gönderme
    client_socket.send(response)
    client_socket.close()
    target_socket.close()

# Help fonksiyonu
def print_help():
    """Kullanıcıya programın nasıl çalıştığına dair bilgi verir."""
    help_text = """
    Snare Proxy Araç Kullanım Kılavuzu:
    
    Bu araç, bir proxy sunucusu gibi çalışarak istemciden gelen istekleri alır ve hedef
    sunucuya ileterek gelen yanıtları işleyip istemciye geri gönderir.
    
    Komutlar:
    - --help veya -h : Yardım metnini görüntüler.
    - --port [port_numarasi] : Proxy'nin dinleyeceği portu belirtir. (Varsayılan: 8080)
    
    Kullanım örneği:
    python snareproxy.py --port 8080
    """
    print(help_text)

# Komut satırı argümanlarını işleyen fonksiyon
def process_args():
    """Komut satırından gelen argümanları işler ve uygulama başlatılmadan önce kontrol eder."""
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)

    if '--port' in sys.argv:
        try:
            port_index = sys.argv.index('--port') + 1
            port = int(sys.argv[port_index])
            if 1024 <= port <= 65535:
                global LISTENING_PORT
                LISTENING_PORT = port
            else:
                print("Port numarası geçersiz, 1024-65535 arasında olmalı.")
                sys.exit(1)
        except (IndexError, ValueError):
            print("Port numarası belirtilmemiş veya geçersiz.")
            sys.exit(1)

# Proxy başlatma
def run_proxy():
    """Proxy sunucusunu başlatır ve gerekli işlemleri yapar."""
    try:
        process_args()  # Argümanları işle
        start_proxy()   # Proxy'yi başlat
    except KeyboardInterrupt:
        print("\nProxy kapatılıyor...")
        exit()

if __name__ == "__main__":
    run_proxy()
