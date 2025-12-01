import requests
import subprocess
import datetime
import os

SERVICE_NAME = "CeladonFlaskService"
HEALTH_URL = "http://127.0.0.1:5000/get-sale"
LOG_FILE = r"C:\CeladonListener\FlaskServer\health_log.txt"
#KILL_FILE = r"Z:\VMStuff\kill.txt"  # shared kill switch file
KILL_FILE = r"\\192.168.2.29\VMStuff:\kill.txt"
NSSM_PATH = r"C:\Windows\System32\nssm.exe"


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
        return False


# Kill switch stops task BEFORE health check
if kill_switch_on():
    log("KILL FLAG ON - Exiting health check.")
    os._exit(0)


# Normal health check:
try:
    r = requests.get(HEALTH_URL, timeout=1)

    if r.status_code == 200:
        log("OK - Flask responded successfully.")

    else:
        log(f"ERROR - Flask returned status {r.status_code}. Restarting service...")
        try:
            subprocess.run([NSSM_PATH, "restart", SERVICE_NAME])
        except Exception as e:
            log(f"FAILED TO RESTART SERVICE: {e}")

except Exception as e:
    log(f"EXCEPTION - {e}. Attempting restart...")
    try:
        subprocess.run([NSSM_PATH, "restart", SERVICE_NAME])
    except Exception as e2:
        log(f"FAILED TO RESTART SERVICE: {e2}")
