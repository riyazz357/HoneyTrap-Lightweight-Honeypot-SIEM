import requests
import random
import time

# The target (Your local Flask trap)
URL = "http://localhost:5000/admin"

# Wordlists (Mini dictionaries)
usernames = ["admin", "root", "sysadmin", "support", "guest", "test"]
passwords = ["123456", "password", "admin123", "qwerty", "letmein", "toor"]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0)",
    "Hydra/9.1 (BruteForce)",
    "Python-urllib/3.9",
    "EvilScript/1.0"
]

print(f"🚀 Launching Brute Force Simulation against {URL}...")

# Run 50 attacks
for i in range(1, 51):
    # 1. Pick random credentials
    u = random.choice(usernames)
    p = random.choice(passwords)
    ua = random.choice(user_agents)

    # 2. Form the payload
    data = {'username': u, 'password': p}
    headers = {'User-Agent': ua}

    try:
        # 3. Fire the request
        response = requests.post(URL, data=data, headers=headers)
        print(f"[{i}] 🔫 Fired: {u}:{p} | Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

    # 4. Sleep briefly (to prevent SQLite locking issues)
    time.sleep(0.1)

print("\n✅ Simulation Complete.")