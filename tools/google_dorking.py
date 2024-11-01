import requests
from bs4 import BeautifulSoup
import csv

# Google arama URL'si
google_url = "https://www.google.com/search"

# Kullanıcıdan alınan anahtar kelimeleri ve operatörleri
def get_user_input():
    anahtar_kelimeler = input("Anahtar kelimeleri girin (örneğin, 'site:.tr'): ")
    return anahtar_kelimeler

# Google'da arama yapma
def google_arama(anahtar_kelimeler):
    params = {"q": anahtar_kelimeler}
    response = requests.get(google_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# Arama sonuçlarını alma
def get_arama_sonuc(soup):
    sonuc = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.startswith("/url?q="):
            sonuc.append(href.split("&sa=U&ved=")[0].replace("/url?q=", ""))
    return sonuc

# Sonuçları filtreleme
def filtrele(sonuc, uzanti):
    filtreli_sonuc = []
    for link in sonuc:
        if link.endswith(uzanti):
            filtreli_sonuc.append(link)
    return filtreli_sonuc

# Sonuçları kaydetme
def kaydet(sonuc, dosya_adi):
    with open(dosya_adi, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Link"])
        for link in sonuc:
            writer.writerow([link])

# Main fonksiyon
def main():
    anahtar_kelimeler = get_user_input()
    soup = google_arama(anahtar_kelimeler)
    sonuc = get_arama_sonuc(soup)
    print("Arama Sonuçları:")
    for link in sonuc:
        print(link)
    
    uzanti = input("Filtrelemek istediğiniz uzantıyı girin (örneğin, '.tr'): ")
    filtreli_sonuc = filtrele(sonuc, uzanti)
    print("Filtreli Sonuçlar:")
    for link in filtreli_sonuc:
        print(link)
    
    dosya_adi = input("Kaydetmek istediğiniz dosya adını girin: ")
    kaydet(filtreli_sonuc, dosya_adi)

if __name__ == "__main__":
    main()
