import socket
import argparse
import threading

# Port Scanning Tool
class PortScanner:
    def __init__(self, target, ports, threads, timeout):
        self.target = target
        self.ports = ports
        self.threads = threads
        self.timeout = timeout
        self.open_ports = []

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.target, port))
            self.open_ports.append(port)
            sock.close()
        except socket.error:
            pass

    def start_scan(self):
        threads = []
        for port in self.ports:
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return self.open_ports

def main():
    parser = argparse.ArgumentParser(description='Port Scanning Tool')
    parser.add_argument('-t', '--target', help='Hedef IP adresi', required=True)
    parser.add_argument('-p', '--ports', help='Tarama yapılacak port aralığı (örneğin: 1-1000)', required=True)
    parser.add_argument('-th', '--threads', help='Kullanılacak thread sayısı', default=10, type=int)
    parser.add_argument('-to', '--timeout', help='Zaman aşımı (saniye)', default=1, type=int)
    args = parser.parse_args()

    target = args.target
    ports = [int(port) for port in range(int(args.ports.split('-')[0]), int(args.ports.split('-')[1]) + 1)]
    threads = args.threads
    timeout = args.timeout

    scanner = PortScanner(target, ports, threads, timeout)
    open_ports = scanner.start_scan()

    print(f'Hedef IP adresi: {target}')
    print(f'Açık portlar:')
    for port in open_ports:
        print(port)

if __name__ == '__main__':
    main()