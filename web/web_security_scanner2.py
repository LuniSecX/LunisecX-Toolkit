import requests
import ssl
import socket
from urllib.parse import urlparse

# HTTP Header taraması
def scan_http_headers(url):
    try:
        response = requests.get(url)
        print(f"\nHTTP Headers for {url}:\n")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: {e}")

# SSL/TLS sertifika taraması
def scan_ssl_tls(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 443  # varsayılan 443 portu

    context = ssl.create_default_context()
    try:
        connection = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        connection.connect((hostname, port))
        ssl_info = connection.getpeercert()

        print(f"\nSSL/TLS Sertifikası Bilgileri for {url}:")
        for key, value in ssl_info.items():
            print(f"{key}: {value}")
        connection.close()
    except Exception as e:
        print(f"SSL/TLS taraması sırasında hata oluştu: {e}")

def main():
    target_url = input("Hedef URL'yi girin (örneğin, https://www.example.com): ")
    
    print(f"\n{target_url} için HTTP header taraması başlatılıyor...")
    scan_http_headers(target_url)

    print(f"\n{target_url} için SSL/TLS taraması başlatılıyor...")
    scan_ssl_tls(target_url)

if __name__ == "__main__":
    main()
