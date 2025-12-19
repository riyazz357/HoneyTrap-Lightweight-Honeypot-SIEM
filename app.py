from flask import Flask, request, render_template_string
import sqlite3
import re  # Regex for pattern matching
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
DB_NAME = "attacks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Added 'attack_type' column
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, ip TEXT, 
                  endpoint TEXT, payload TEXT, user_agent TEXT, attack_type TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- DEFENSE LOGIC: The WAF (Web App Firewall) ---
def analyze_payload(data_string):
    """Checks for common SQL Injection signatures"""
    # Patterns: Single quotes, comments (--), UNION statements
    sqli_patterns = [
        r"'.*OR.*'='",   # ' OR '1'='1
        r"'.*--",        # ' --
        r"UNION SELECT", # database combining
        r"@@version",    # version fingerprinting
        r"waitfor delay" # time-based attacks
    ]
    
    for pattern in sqli_patterns:
        if re.search(pattern, data_string, re.IGNORECASE):
            return "SQL_INJECTION"
            
    return "BRUTE_FORCE" # Default for login attempts

# --- ROUTES ---

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        ip = request.remote_addr # Remember to add the ngrok patch here if using ngrok
        username = request.form.get('username')
        password = request.form.get('password')
        payload = f"User: {username} | Pass: {password}"
        
        # Log it as Brute Force
        log_attack(ip, '/admin', payload, "BRUTE_FORCE", request.headers.get('User-Agent'))
        
        return "Internal Server Error: DB_CONNECTION_TIMEOUT", 500
    
    return """
    <h2>Admin Login</h2>
    <form method=post>
      <input type=text name=username placeholder="Username"><br>
      <input type=password name=password placeholder="Password"><br>
      <input type=submit value=Login>
    </form>
    """

@app.route('/search', methods=['GET'])
def search_page():
    query = request.args.get('q')
    
    if query:
        # Check if they are attacking
        attack_type = "RECON" # Default: just looking around
        
        # If the WAF detects bad characters, upgrade severity
        if analyze_payload(query) == "SQL_INJECTION":
            attack_type = "SQL_INJECTION"
            
        log_attack(request.remote_addr, '/search', f"Query: {query}", attack_type, request.headers.get('User-Agent'))
        
        return f"No results found for '{query}'."

    return """
    <h2>Employee Directory Search</h2>
    <form method=get>
      <input type=text name=q placeholder="Search by name...">
      <input type=submit value=Search>
    </form>
    """

def log_attack(ip, endpoint, payload, attack_type, user_agent):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, ip, endpoint, payload, user_agent, attack_type) VALUES (?, ?, ?, ?, ?, ?)",
              (timestamp, ip, endpoint, payload, user_agent, attack_type))
    conn.commit()
    conn.close()
    print(f"[{attack_type}] {ip} -> {payload}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)