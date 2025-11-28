import requests
import subprocess
import datetime

SERVICE_NAME = "CeladonFlaskService"
HEALTH_URL = "http://127.0.0.1:5000/get-sale"
LOG_FILE = r"C:\CeladonListener\FlaskServer\health_log.txt"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {msg}\n")

try:
    r = requests.get(HEALTH_URL, timeout=1)
    if r.status_code == 200:
        log("OK - Flask responded successfully.")
    else:
        log(f"ERROR - Flask returned status {r.status_code}. Restarting service...")
        subprocess.run(["nssm", "restart", SERVICE_NAME])
except Exception as e:
    log(f"EXCEPTION - {e}. Restarting service...")
    subprocess.run(["nssm", "restart", SERVICE_NAME])
