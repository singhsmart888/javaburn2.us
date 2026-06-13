"""
Bing IndexNow - Instant Indexing Submission for javaburn2.us
Usage: python submit-indexnow.py
"""

import os
import re
import urllib.request
import json

API_KEY = "5e1086823d50d977d0b3bbc72b71ac1b"
HOST = "javaburn2.us"
SITEMAP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "sitemap.xml")
ENDPOINT = "https://api.indexnow.org/indexnow"

# Read URLs from local sitemap.xml
with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
    sitemap = f.read()

URLS = sorted(set(re.findall(r"https://javaburn2\.us[^<]+", sitemap)))

payload = json.dumps({
    "host": HOST,
    "key": API_KEY,
    "keyLocation": f"https://{HOST}/{API_KEY}.txt",
    "urlList": URLS
}).encode("utf-8")

req = urllib.request.Request(
    ENDPOINT,
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST"
)

print(f"Submitting {len(URLS)} URLs to Bing IndexNow...")
print(f"Key: {API_KEY}")
print(f"Key file: https://{HOST}/{API_KEY}.txt")
print()

try:
    with urllib.request.urlopen(req) as resp:
        status = resp.status
        body = resp.read().decode()
        print(f"Response: {status}")
        if body:
            print(body)
        if status == 200:
            print("\nSUCCESS — Bing ne URLs accept kar liye!")
        elif status == 202:
            print("\nACCEPTED (202) — URLs queue me hain, Bing indexing karega.")
        else:
            print(f"\nStatus {status} — Check Bing Webmaster Tools.")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP Error {e.code}: {e.reason}")
    print(body)
    if e.code == 403:
        print("\nERROR 403: Key file domain pe accessible nahi hai.")
        print(f"Check: https://{HOST}/{API_KEY}.txt")
    elif e.code == 422:
        print("\nERROR 422: URLs invalid hain ya domain match nahi karta.")
