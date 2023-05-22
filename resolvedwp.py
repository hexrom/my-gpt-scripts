import sys
import socket
import requests
import time

def resolve_domains_from_file(file_path, wordpress_paths_file):
    # Open the file containing the list of domains
    with open(file_path, 'r') as file:
        domains = file.read().splitlines()

    # Resolve domains and fuzz WordPress paths for the resolved domains
    resolved_domains = resolve_domains(domains)
    fuzz_wordpress_paths(resolved_domains, wordpress_paths_file)

def resolve_domains(domains):
    resolved_domains = []
    for domain in domains:
        try:
            time.sleep(1)  # Wait for 1 second before resolving the domain
            ip_address = socket.gethostbyname(domain)
            print(f"Domain '{domain}' resolved successfully. IP: {ip_address}")
            resolved_domains.append(domain)
        except socket.timeout:
            print(f"Domain '{domain}' timed out.")
        except socket.gaierror:
            print(f"Failed to resolve domain '{domain}'.")
    return resolved_domains

def load_wordpress_paths(file_path):
    # Open the file containing the WordPress paths
    with open(file_path, 'r') as file:
        paths = file.read().splitlines()
    return paths

def fuzz_wordpress_paths(domains, wordpress_paths_file):
    paths = load_wordpress_paths(wordpress_paths_file)

    for domain in domains:
        print(f"--- Fuzzing WordPress Paths for Domain: {domain} ---")
        for path in paths:
            url = f"http://{domain}{path}"
            time.sleep(2)  # Wait for 2 seconds before fuzzing the next path
            response = requests.get(url, allow_redirects=False)
            if response.status_code == 200:
                print(f"Found WordPress path: {url}")
            elif response.status_code == 302:
                print(f"302 redirect encountered. Skipping path: {url}")
        print()

# Example usage
if len(sys.argv) < 3:
    print("Usage: python script.py <file_path> <wordpress_paths_file>")
    sys.exit(1)

file_path = sys.argv[1]
wordpress_paths_file = sys.argv[2]
resolve_domains_from_file(file_path, wordpress_paths_file)





