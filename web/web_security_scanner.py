import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

class WebSecurityScanner:
    def __init__(self, url):
        self.url = url
        self.results = []
    
    def send_request(self, endpoint=""):
        """Web sunucusuna GET isteği gönderir ve yanıtı döndürür."""
        try:
            full_url = self.url + endpoint
            response = requests.get(full_url)
            if response.status_code == 200:
                return response
            else:
                print(f"Hata: {full_url} {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"İstek hatası: {e}")
            return None

    def test_sql_injection(self):
        """SQL Enjeksiyonu açığını test eder."""
        payload = "' OR 1=1 --"
        encoded_payload = quote(payload)  # Payload'ı URL encode ediyoruz
        test_url = f"{self.url}{encoded_payload}"
        response = self.send_request(encoded_payload)
        if response and "error" in response.text:
            self.results.append(f"SQL Injection Açığı Tespit Edildi: {test_url}")
        else:
            self.results.append(f"SQL Injection testi başarılı: {test_url}")

    def test_xss(self):
        """XSS açığını test eder."""
        payload = "<script>alert('XSS');</script>"
        encoded_payload = quote(payload)  # Payload'ı URL encode ediyoruz
        test_url = f"{self.url}{encoded_payload}"
        response = self.send_request(encoded_payload)
        if response and payload in response.text:
            self.results.append(f"XSS Açığı Tespit Edildi: {test_url}")
        else:
            self.results.append(f"XSS testi başarılı: {test_url}")

    def check_security_headers(self):
        """Güvenlik başlıklarını kontrol eder."""
        response = self.send_request()
        if response:
            headers = response.headers
            important_headers = ['Strict-Transport-Security', 'X-Content-Type-Options', 'X-Frame-Options']
            for header in important_headers:
                if header not in headers:
                    self.results.append(f"Güvenlik Başlığı Eksik: {header}")
                else:
                    self.results.append(f"{header} Başlığı Var.")

    def test_default_pages(self):
        """Varsayılan sunucu sayfalarını kontrol eder."""
        common_default_pages = ['/admin', '/test', '/login', '/index.php']
        for page in common_default_pages:
            response = self.send_request(page)
            if response:
                self.results.append(f"Varsayılan Sayfa Bulundu: {self.url}{page}")
            else:
                self.results.append(f"Varsayılan Sayfa Yok: {self.url}{page}")

    def run_scan(self):
        """Taramayı başlatır ve tüm testleri çalıştırır."""
        print(f"Taramaya Başlandı: {self.url}")
        self.test_sql_injection()
        self.test_xss()
        self.check_security_headers()
        self.test_default_pages()

    def write_report(self):
        """Sonuçları dosyaya kaydeder."""
        with open('security_report.txt', 'w') as file:
            file.write(f"Web Güvenlik Tarayıcı Raporu - {self.url}\n\n")
            for result in self.results:
                file.write(f"{result}\n")
        print("Rapor kaydedildi: security_report.txt")

    def display_results(self):
        """Tarama sonuçlarını ekranda görüntüler."""
        print(f"Tarama Sonuçları: {self.url}")
        for result in self.results:
            print(result)

if __name__ == "__main__":
    # Kullanıcıdan URL al
    url = input("Taramak için URL girin (örneğin: http://example.com): ")
    
    # Scanner'ı başlat
    scanner = WebSecurityScanner(url)
    
    # Taramayı başlat
    scanner.run_scan()
    
    # Sonuçları yazdır
    scanner.display_results()
    
    # Raporu kaydet
    scanner.write_report()
