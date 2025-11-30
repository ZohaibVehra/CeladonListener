import subprocess
import datetime
import os

SERVICE_NAME = "TestKillService"
LOG_FILE = r"C:\CeladonListener\health_test_log.txt"

# Shared kill-switch file
KILL_FILE = r"Z:\kill.txt"


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
        return False  # missing file = treat as run


def is_service_running():
    """Return True if the NSSM service is currently running."""
    try:
        result = subprocess.run(
            ["nssm", "status", SERVICE_NAME],
            capture_output=True,
            text=True
        )
        return "SERVICE_RUNNING" in result.stdout
    except Exception as e:
        log(f"EXCEPTION checking service status: {e}")
        return False


# ----------------------------------------------------
# KILL-SWITCH CHECK FIRST
# ----------------------------------------------------
if kill_switch_on():
    log("KILL FLAG ON - Not restarting TestKillService.")
    exit(0)  # normal exit so Task Scheduler doesn't complain


# ----------------------------------------------------
# NORMAL HEALTH CHECK FOR TestKillService
# ----------------------------------------------------
if is_service_running():
    log("OK - TestKillService is running normally.")
else:
    log("Service is NOT running - Restarting TestKillService...")
    subprocess.run(["nssm", "restart", SERVICE_NAME])
