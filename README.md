---

## ⚙️ Features

- ✅ WHOIS lookup — domain owner, registrar, dates
- ✅ DNS records — A, NS, MX, TXT
- ✅ Geolocation — country, city, lat/long
- ✅ Shodan IP lookup — open ports, banners, org
- ✅ Save results to a file

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/তোমার_username/infogather.git
cd infogather
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---
## 🔑 Shodan API Key Setup

1. Register at 👉 [https://account.shodan.io/register](https://account.shodan.io/register)
2. Go to 👉 [https://account.shodan.io](https://account.shodan.io)
3. Copy your API key
4. Open `info_gathering.py` and replace:
```python
SHODAN_API_KEY = "api_key"
```

---

## 🚀 Usage
```bash
# Only WHOIS + DNS + Geolocation
python3 info_gathering.py -d google.com

# With Shodan IP lookup
python3 info_gathering.py -d google.com -s 8.8.8.8

# Save results to file
python3 info_gathering.py -d google.com -o result.txt

# All together
python3 info_gathering.py -d google.com -s 8.8.8.8 -o result.txt
```

### Arguments

| Flag | Long | Description |
|------|------|-------------|
| `-d` | `--domain` | Target domain name |
| `-s` | `--shodan` | IP address for Shodan lookup |
| `-o` | `--output` | Output file to save results |
---
