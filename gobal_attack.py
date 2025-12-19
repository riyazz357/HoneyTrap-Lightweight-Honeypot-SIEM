import sqlite3
import random
from datetime import datetime

# --- FAKE FOREIGN ATTACKERS ---
# These are real IPs from Russia, China, USA, Brazil, Germany
foreign_ips = [
    "103.21.244.0",  # Vietnam
    "185.220.101.0", # Germany (Tor Exit Node)
    "45.83.67.1",    # Russia
    "221.192.199.9", # China
    "192.168.1.5",   # USA
    "177.12.5.1"     # Brazil
]

payloads = ["' OR 1=1 --", "admin:12345", "root:toor", "SELECT * FROM users"]
types = ["SQL_INJECTION", "BRUTE_FORCE", "RECON"]
user_agents = ["Mozilla/5.0", "Hydra", "Sqlmap"]

print("🌍 Simulating Global Cyber War...")

conn = sqlite3.connect('attacks.db')
c = conn.cursor()

for _ in range(20):
    ip = random.choice(foreign_ips)
    payload = random.choice(payloads)
    attack = random.choice(types)
    ua = random.choice(user_agents)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("INSERT INTO logs (timestamp, ip, endpoint, payload, user_agent, attack_type) VALUES (?, ?, ?, ?, ?, ?)",
              (timestamp, ip, '/simulated', payload, ua, attack))
    print(f"💥 Attack from {ip} logged.")

conn.commit()
conn.close()
print("✅ Database populated with international threats.")