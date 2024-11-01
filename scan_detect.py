from tools.subdomain_enum import subdomain_enum
from tools.google_dorking import google_dorking

def main():
    print("1. Subdomain Enum")
    print("2. Google Dorking")
    secim = input("Seçim yapın: ")

    if secim == "1":
        domain = input("Domain girin: ")
        wordlist = input("Wordlist dosyası girin: ")
        output_file = input("Çıktı dosyası girin: ")
        subdomain_enum.subdomain_enum(domain, wordlist, output_file)
    elif secim == "2":
        anahtar_kelimeler = input("Anahtar kelimeleri girin: ")
        uzanti = input("Filtrelemek istediğiniz uzantıyı girin: ")
        dosya_adi = input("Kaydetmek istediğiniz dosya adını girin: ")
        google_dorking.google_dorking(anahtar_kelimeler, uzanti, dosya_adi)
    else:
        print("Geçersiz seçim")

if __name__ == '__main__':
    main()