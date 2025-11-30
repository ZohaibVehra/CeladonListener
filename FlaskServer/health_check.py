import requests
import subprocess
import datetime
import os

SERVICE_NAME = "CeladonFlaskService"
HEALTH_URL = "http://127.0.0.1:5000/get-sale"
LOG_FILE = r"C:\CeladonListener\FlaskServer\health_log.txt"

KILL_FILE = r"Z:\VMStuff\kill.txt"  # shared kill switch file


def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {msg}\n")


def kill_switch_on():
    """Return True if kill.txt contains 'kill'."""
    try:
        with open(KILL_FILE, "r") as f:
            content = f.read().strip().lower()
            return content == "kill"
    except:
        return False  # If file missing or unreadable → treat as "run"


# 🔥 BEFORE doing any health checks, honor kill.txt
if kill_switch_on():
    log("KILL FLAG ON - Not restarting service. Exiting health check.")
    exit(0)


# ------------------------------------------
# Normal health check below
# ------------------------------------------

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
