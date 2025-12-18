from flask import Flask, request, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, ip TEXT, 
                  endpoint TEXT, payload TEXT, user_agent TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- The Trap ---
# We use a simple HTML template inside the code for simplicity
LOGIN_PAGE = """
<!doctype html>
<title>Secure Admin Portal</title>
<style>body { font-family: sans-serif; text-align: center; padding-top: 50px; }</style>
<h2>System Administration Login</h2>
<form method=post>
  <input type=text name=username placeholder="Username" required><br><br>
  <input type=password name=password placeholder="Password" required><br><br>
  <input type=submit value=Login>
</form>
<p style="color:red; font-size: small;">Authorized Personnel Only</p>
"""

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # CAPTURE THE DATA
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        username = request.form.get('username')
        password = request.form.get('password')
        payload = f"User: {username} | Pass: {password}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # LOG IT TO DATABASE
        conn = sqlite3.connect('attacks.db')
        c = conn.cursor()
        c.execute("INSERT INTO logs (timestamp, ip, endpoint, payload, user_agent) VALUES (?, ?, ?, ?, ?)",
                  (timestamp, ip, '/admin', payload, user_agent))
        conn.commit()
        conn.close()
        
        print(f"[!] ATTACK DETECTED from {ip}: {payload}") # Print to console for immediate feedback
        
        return "Internal Server Error: DB_CONNECTION_TIMEOUT", 500
    
    return render_template_string(LOGIN_PAGE)

@app.route('/')
def index():
    return "Welcome to the Company Homepage. Nothing to see here."

if __name__ == '__main__':
    # Run on 0.0.0.0 to make it accessible to other devices on your WiFi
    app.run(host='0.0.0.0', port=5000, debug=True)