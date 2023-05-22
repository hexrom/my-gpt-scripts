import socket
import requests
import time

def resolve_domains_from_file(file_path):
    # Open the file containing the list of domains
    with open(file_path, 'r') as file:
        domains = file.read().splitlines()

    # Resolve domains and detect CMS for the resolved domains
    resolved_domains = resolve_domains(domains)
    detect_cms(resolved_domains)

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

def detect_cms(domains):
    for domain in domains:
        try:
            url = f"https://whatcms.org/?s={domain}"
            time.sleep(3)  # Wait for 3 seconds before making the API request
            response = requests.get(url)
            if response.ok:
                data = response.json()
                if data and 'result' in data and 'name' in data['result']:
                    cms = data['result']['name']
                    print(f"Domain '{domain}' CMS: {cms}")
                else:
                    print(f"No CMS detected for domain '{domain}'.")
            else:
                print(f"Failed to detect CMS for domain '{domain}'. Status Code: {response.status_code}")
        except (requests.RequestException, ValueError) as e:
            print(f"Failed to detect CMS for domain '{domain}'. Error: {str(e)}")

# Example usage
file_path = 'domains.txt'  # Replace with the path to your domain list file
resolve_domains_from_file(file_path)



