# Vine Forcer

Vine Forcer is a fast, multi-purpose async tool for web penetration testers.  
It supports:
- URL status checking
- Subdomain enumeration
- Brute-force attacks (URL, headers, cookies, body)
- Built-in async listener

## Features
- Ultra-fast async requests using Python `httpx` & `asyncio`
- Flexible brute-force templates
- Multi-mode: status checker, subdomain enum, bruteforce, listener
- Easy CLI usage

## Installation
```bash
git clone https://github.com/yourusername/vine-forcer.git
cd vine-forcer
pip install -r requirements.txt


# Check URL status
vine -u https://example.com -m 1

# Subdomain enumeration
vine -u example.com -m 2 -w wordlist.txt

# Bruteforce FUZZ in URL
vine -u https://example.com/FUZZ -m 3 -w wordlist.txt

# Bruteforce headers, cookies, body
vine -u https://example.com/api -m 3 -he "Authorization: Bearer FUZZ" -co "session=FUZZ" -b "username=FUZZ&password=123" -x POST -w wordlist.txt

# Start listener
vine -ip 0.0.0.0 -l 9999 -m 4