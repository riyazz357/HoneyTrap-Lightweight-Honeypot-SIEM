# 🍯 HoneyTrap: Lightweight Honeypot & SIEM

**HoneyTrap** is a mid-level cybersecurity project designed to detect, log, and analyze unauthorized access attempts. It functions as a "Blue Team" tool that deploys a vulnerable-looking web application (the Decoy) to lure attackers and captures their innovative payloads, IP addresses, and user agents for analysis.

## 🏗 Architecture
The project consists of three core components:
1.  **The Decoy (Flask):** A fake "Admin Portal" designed to look sensitive to attract brute-force attacks.
2.  **The Logger (SQLite):** A silent middleware that captures request headers and POST data.
3.  **The SIEM (Streamlit):** *[In Development]* A dashboard to visualize attack patterns and threat intelligence.

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Web Framework:** Flask
* **Database:** SQLite3
* **Visualization:** Streamlit (Phase 2)

## 📂 Project Structure
```bash
HoneyTrap/
├── app.py              # The Flask Decoy application
├── attacks.db          # SQLite database (auto-generated)
├── dashboard.py        # Streamlit SIEM (Coming in Phase 2)
└── README.md           # Documentation

pip install flask pandas streamlit

python app.py
