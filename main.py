import whois
import dns.resolver
import shodan
import requests
import argparse
import socket
import io
import sys

# Argument parser
parser = argparse.ArgumentParser(
    description="Basic Info Gathering Tool",
    usage="python3 info_gathering.py -d <domain> [-s <IP>] [-o <output_file>]"
)
parser.add_argument("-d", "--domain", help="Enter the domain name for footprinting.")
parser.add_argument("-s", "--shodan", help="Enter the IP address for Shodan lookup.")
parser.add_argument("-o", "--output", help="Enter the output file name to save results.")

args = parser.parse_args()
domain = args.domain
ip = args.shodan
output = args.output

if not domain:
    print("[-] Please provide a domain using -d flag.")
    exit()

# Output capture করার জন্য
all_results = []

def log(text=""):
    print(text)
    all_results.append(text)

# ─── WHOIS ───────────────────────────────────────────────
log("\n[+] Getting WHOIS info ...")
try:
    w = whois.whois(domain)
    log("[+] WHOIS info found")
    log(f"    domain_name    : {w.get('domain_name')}")
    log(f"    registrar      : {w.get('registrar')}")
    log(f"    creation_date  : {w.get('creation_date')}")
    log(f"    expiration_date: {w.get('expiration_date')}")
    log(f"    name_servers   : {w.get('name_servers')}")
except Exception as e:
    log(f"[-] WHOIS failed: {e}")

# ─── DNS ─────────────────────────────────────────────────
log("\n[+] Getting DNS info ...")
for record_type in ['A', 'NS', 'MX', 'TXT']:
    try:
        answers = dns.resolver.resolve(domain, record_type)
        for rdata in answers:
            log(f"    [+] {record_type} Record: {rdata.to_text()}")
    except Exception:
        log(f"    [-] No {record_type} records found.")

# ─── GEOLOCATION ─────────────────────────────────────────
log("\n[+] Getting Geolocation info ...")
try:
    resolved_ip = socket.gethostbyname(domain)
    response = requests.get(f"https://geolocation-db.com/json/{resolved_ip}", timeout=5).json()
    log(f"    [+] IP        : {resolved_ip}")
    log(f"    [+] Country   : {response.get('country_name', 'N/A')}")
    log(f"    [+] Latitude  : {response.get('latitude', 'N/A')}")
    log(f"    [+] Longitude : {response.get('longitude', 'N/A')}")
    log(f"    [+] City      : {response.get('city', 'N/A')}")
    log(f"    [+] State     : {response.get('state', 'N/A')}")
except Exception as e:
    log(f"[-] Geolocation failed: {e}")

# ─── SHODAN ──────────────────────────────────────────────
if ip:
    log("\n[+] Running Shodan IP Lookup ...")
    SHODAN_API_KEY = "তোমার_api_key_এখানে"  # 👈 এইটা বদলাও
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        result = api.host(ip)
        log(f"    [+] IP      : {result['ip_str']}")
        log(f"    [+] Org     : {result.get('org', 'N/A')}")
        log(f"    [+] OS      : {result.get('os', 'N/A')}")
        log(f"    [+] Country : {result.get('country_name', 'N/A')}")
        for item in result['data']:
            log(f"\n    [+] Port   : {item['port']}")
            log(f"    [+] Banner :\n{item['data']}")
    except shodan.APIError as e:
        log(f"[-] Shodan failed: {e}")

# ─── OUTPUT FILE ─────────────────────────────────────────
if output:
    try:
        with open(output, 'w') as file:
            file.write('\n'.join(all_results))
        print(f"\n[+] Results saved to: {output}")
    except Exception as e:
        print(f"[-] File write failed: {e}")
