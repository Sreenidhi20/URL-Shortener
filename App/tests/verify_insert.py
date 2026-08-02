import json
import urllib.request

payload = json.dumps({"url": "https://example.com", "expiry_days": 1}).encode()
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/shorten",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as response:
    print(response.read().decode())
