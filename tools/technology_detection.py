import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
import asyncio

# Web sitesinin HTML kodunu almak
async def get_html(url):
    try:
        print(f"Web sitesinin HTML kodunu almak için istek gönderiliyor... ({url})")
        response = requests.get(url)
        print(f"İstek gönderildi. Durum kodu: {response.status_code}")
        if response.status_code == 200:
            print("HTML kodu alındı.")
            return response.text, response.headers
        else:
            print(f"Hata: {response.status_code} durum kodu ile karşılaşıldı.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Hata: {e}")
        return None, None

# HTML kodunu parse etmek
async def parse_html(html):
    try:
        print("HTML kodunu parse etmek...")
        soup = BeautifulSoup(html, 'html.parser')
        print("HTML kodu parse edildi.")
        return soup
    except Exception as e:
        print(f"Hata: {e}")
        return None

# Teknolojileri tespit etmek
async def detect_technologies(soup, headers):
    try:
        print("Teknolojileri tespit etmek...")
        technologies = set()
        
        # Web sunucusu
        print("Web sunucusu tespit ediliyor...")
        server_header = headers.get('Server')
        if server_header:
            technologies.add(f"Web Sunucusu: {server_header}")
            print(f"Web sunucusu tespit edildi: {server_header}")
        else:
            print("Web sunucusu tespit edilemedi.")
        
        # İşletim sistemi
        print("İşletim sistemi tespit ediliyor...")
        os_header = headers.get('X-Powered-By')
        if os_header:
            technologies.add(f"İşletim Sistemi: {os_header}")
            print(f"İşletim sistemi tespit edildi: {os_header}")
        else:
            print("İşletim sistemi tespit edilemedi.")
        
        # Programlama dili
        print("Programlama dili tespit ediliyor...")
        lang_header = headers.get('X-Powered-By')
        if lang_header:
            technologies.add(f"Programlama Dili: {lang_header}")
            print(f"Programlama dili tespit edildi: {lang_header}")
        else:
            print("Programlama dili tespit edilemedi.")
        
        # Veritabanı yönetim sistemi
        print("Veritabanı yönetim sistemi tespit ediliyor...")
        db_header = headers.get('X-Database')
        if db_header:
            technologies.add(f"Veritabanı Yönetim Sistemi: {db_header}")
            print(f"Veritabanı yönetim sistemi tespit edildi: {db_header}")
        else:
            print("Veritabanı yönetim sistemi tespit edilemedi.")
        
        # Framework'ler
        print("Framework'ler tespit ediliyor...")
        framework_headers = soup.find_all('meta', attrs={'name': 'framework'})
        for framework_header in framework_headers:
            framework = framework_header.get('content')
            technologies.add(f"Framework: {framework}")
            print(f"Framework tespit edildi: {framework}")
        
        # Kütüphaneler
        print("Kütüphaneler tespit ediliyor...")
        library_headers = soup.find_all('meta', attrs={'name': 'library'})
        for library_header in library_headers:
            library = library_header.get('content')
            technologies.add(f"Kütüphane: {library}")
            print(f"Kütüphane tespit edildi: {library}")
        
        # JavaScript kütüphaneleri
        print("JavaScript kütüphaneleri tespit ediliyor...")
        script_tags = soup.find_all('script')
        for script_tag in script_tags:
            script_src = script_tag.get('src')
            if script_src:
                if 'jquery' in script_src.lower():
                    technologies.add("JavaScript Kütüphanesi: jQuery")
                    print("JavaScript kütüphanesi tespit edildi: jQuery")
                elif 'react' in script_src.lower():
                    technologies.add("JavaScript Kütüphanesi: React")
                    print("JavaScript kütüphanesi tespit edildi: React")
                elif 'angular' in script_src.lower():
                    technologies.add("JavaScript Kütüphanesi: Angular")
                    print("JavaScript kütüphanesi tespit edildi: Angular")
                elif 'vue' in script_src.lower():
                    technologies.add("JavaScript Kütüphanesi: Vue.js")
                    print("JavaScript kütüphanesi tespit edildi: Vue.js")
        
        # CSS framework'leri
        print("CSS framework'leri tespit ediliyor...")
        link_tags = soup.find_all('link')
        for link_tag in link_tags:
            link_href = link_tag.get('href')
            if link_href:
                if 'bootstrap' in link_href.lower():
                    technologies.add("CSS Framework: Bootstrap")
                    print("CSS framework tespit edildi: Bootstrap")
                elif 'materialize' in link_href.lower():
                    technologies.add("CSS Framework: Materialize")
                    print("CSS framework tespit edildi: Materialize")
                elif 'tailwind' in link_href.lower():
                    technologies.add("CSS Framework: Tailwind CSS")
                    print("CSS framework tespit edildi: Tailwind CSS")
        
        # CDN'ler
        print("CDN'ler tespit ediliyor...")
        script_tags = soup.find_all('script')
        for script_tag in script_tags:
            script_src = script_tag.get('src')
            if script_src:
                if 'cdn' in script_src.lower():
                    technologies.add(f"CDN: {script_src}")
                    print(f"CDN tespit edildi: {script_src}")
        
        print("Teknolojiler tespit edildi.")
        return technologies
    except Exception as e:
        print(f"Hata: {e}")
        return None

# Sonuçları ekrana yazdırmak
async def print_results(technologies):
    try:
        print("Sonuçlar:")
        for technology in technologies:
            print(technology)
    except Exception as e:
        print(f"Hata: {e}")

# Main fonksiyon
async def main():
    try:
        url = "https://www.youtube.com"
        print(f"Web sitesi URL'si girildi: {url}")
        html, headers = await get_html(url)
        if html:
            soup = await parse_html(html)
            if soup:
                technologies = await detect_technologies(soup, headers)
                if technologies:
                    await print_results(technologies)
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    asyncio.run(main())