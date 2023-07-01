import sys
import requests
import socket

def check_web_service(ip, port):
    try:
        url = f"http://{ip}:{port}"
        response = requests.get(url, timeout=2)
        
        if response.status_code == 200:
            domain = get_domain(ip)
            print(f"IP: {ip} - Domain: {domain} - Port: {port} is open")
            with open("open_ports.txt", "a") as f:
                f.write(f"{ip}:{port} - Domain: {domain}\n")
        else:
            print(f"IP: {ip} - Port: {port} is closed")
    except requests.RequestException as e:
        print(f"Error: {e}")

def get_domain(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def get_ip_addresses(as_number):
    try:
        url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{as_number}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            prefixes = data["data"]["prefixes"]
            
            ip_addresses = []
            for prefix in prefixes:
                ip_range = prefix["prefix"]
                ip_addresses.extend(get_ip_range(ip_range))
            
            return ip_addresses
        else:
            print(f"Error: Unable to retrieve data for AS{as_number}")
            return []
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []

def get_ip_range(ip_range):
    ip_range_parts = ip_range.split("/")
    network_address = ip_range_parts[0]
    prefix_length = int(ip_range_parts[1])
    
    ip_addresses = []
    if prefix_length < 32:
        num_addresses = 2 ** (32 - prefix_length)
        for i in range(num_addresses):
            ip_address = long_to_ip(ip_to_long(network_address) + i)
            ip_addresses.append(ip_address)
    else:
        ip_addresses.append(network_address)
    
    return ip_addresses

def ip_to_long(ip_address):
    ip_parts = ip_address.split(".")
    long_ip = 0
    for i, part in enumerate(ip_parts):
        long_ip += int(part) << (24 - 8 * i)
    return long_ip

def long_to_ip(long_ip):
    ip_parts = []
    for i in range(4):
        ip_parts.append(str(long_ip >> (24 - 8 * i) & 255))
    return ".".join(ip_parts)

if len(sys.argv) < 2:
    print("AS number argument is missing.")
    sys.exit(1)

# AS number to retrieve IP addresses for
as_number = sys.argv[1]

# Get all IP addresses in all netblocks of the AS number
ip_addresses = get_ip_addresses(as_number)

# Save IP addresses to ips.txt
with open("ips.txt", "w") as f:
    for ip in ip_addresses:
        f.write(ip + "\n")

# Ports to check (HTTP and HTTPS)
ports = [80, 443, 8080, 8443, 8000, 8008, 8888]

# Iterate over each IP address and port combination
for ip in ip_addresses:
    for port in ports:
        check_web_service(ip, port)
