import requests,dns.resolver,argparse,threading,re,time
from concurrent.futures import ThreadPoolExecutor

# Subdomain keşfetme yöntemleri
def dns_brute_force(domain, wordlist, output_file, progress_callback):
    """
    DNS brute force ile subdomain keşfetme
    """
    print(f"[+] DNS Brute Force saldırısı başlatıldı: {domain}")
    try:
        with open(wordlist, 'r') as f:
            lines = f.readlines()
            total_lines = len(lines)
            processed_lines = 0

            def check_subdomain(line):
                nonlocal processed_lines
                subdomain = line.strip() + '.' + domain
                try:
                    answers = dns.resolver.resolve(subdomain, 'A', lifetime=10)
                    for rdata in answers:
                        if subdomain not in open(output_file).read():
                            with open(output_file, 'a') as output:
                                output.write(subdomain + '\n')
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout):
                    pass
                processed_lines += 1
                progress_callback("DNS Brute Force", processed_lines, total_lines)

            with ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(check_subdomain, lines)

    except FileNotFoundError:
        print("Wordlist dosyası bulunamadı.")

def dns_zone_transfer(domain, output_file, progress_callback):
    """
    DNS zone transfer ile subdomain keşfetme
    """
    print(f"[+] DNS Zone Transfer saldırısı başlatıldı: {domain}")
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        total_servers = len(answers)
        processed_servers = 0
        for rdata in answers:
            ns_server = str(rdata)
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns_server, domain))
                for name, ttl, rdata in zone.iterate_rdatas('A'):
                    subdomain = str(name) + '.' + domain
                    if subdomain not in open(output_file).read():
                        with open(output_file, 'a') as output:
                            output.write(subdomain + '\n')
            except (dns.query.TransferError, ValueError, dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                pass
            processed_servers += 1
            progress_callback("DNS Zone Transfer", processed_servers, total_servers)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        print(f"[-] {domain} adresine cevap alınamadı.")

def crt_sh(domain, output_file, progress_callback):
    """
    crt.sh kullanarak subdomain keşfetme
    """
    print(f"[+] crt.sh sorgusu başlatıldı: {domain}")
    url = f"https://crt.sh/?q={domain}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            total_lines = len(lines)
            processed_lines = 0
            for line in lines:
                if domain in line:
                    try:
                        subdomain = line.split()[4]
                        if re.match(r'^[a-zA-Z0-9.-]+\.' + domain + '$', subdomain):
                            if subdomain not in open(output_file).read():
                                with open(output_file, 'a') as output:
                                    output.write(subdomain + '\n')
                    except IndexError:
                        pass
                processed_lines += 1
                progress_callback("crt.sh Sorgusu", processed_lines, total_lines)
        else:
            pass
    except requests.exceptions.RequestException as e:
        pass

def progress_callback(method, processed, total):
    percent = round((processed / total) * 100,2)
    print(f"[+] {method} İlerleme: %{percent}       ",end='\r')

def main():
    parser = argparse.ArgumentParser(description='Subdomain Enumeration Programı')
    parser.add_argument('-d', '--domain', help='Alan adı', required=True)
    parser.add_argument('-w', '--wordlist', help='Wordlist dosyası')
    parser.add_argument('-o', '--output', help='Çıktı dosyası', default='subdomains.txt')
    args = parser.parse_args()

    domain = args.domain
    output_file = args.output

    start_time = time.time()

    # DNS brute force ile subdomain keşfetme
    if args.wordlist:
        t1 = threading.Thread(target=dns_brute_force, args=(domain, args.wordlist, output_file, progress_callback))
        t1.daemon = True
        t1.start()

    # DNS zone transfer ile subdomain keşfetme
    t2 = threading.Thread(target=dns_zone_transfer, args=(domain, output_file, progress_callback))
    t2.daemon = True
    t2.start()

    # crt.sh kullanarak subdomain keşfetme
    t3 = threading.Thread(target=crt_sh, args=(domain, output_file, progress_callback))
    t3.daemon = True
    t3.start()

    # Thread'lerin sonlanmasını bekle
    while threading.active_count() > 1:
        pass

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n[+] İşlem tamamlandı. Geçen süre: {elapsed_time:.2f} saniye")

    print(f"[+] Subdomain'ler {output_file} dosyasına kaydedildi.")

if __name__ == '__main__':
    main()