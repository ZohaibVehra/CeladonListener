import subprocess
import time
import psutil
import os
import sys

#KILL_FILE = r"Z:\kill.txt"
KILL_FILE = r"\\VBOXSVR\VMStuff\kill.txt"

DISCORD_READER_PATH = r"C:\CeladonListener\discordReader.py"
PYTHON_EXE = r"C:\Users\zzoha\AppData\Local\Programs\Python\Python310\python.exe"

with open(r"C:\CeladonListener\monitor_debug.txt","a") as f:
    f.write("MONITOR STARTED\n")

def kill_switch_on():
    try:
        with open(KILL_FILE, "r") as f:
            return f.read().strip().lower() == "kill"
    except:
        return False


def is_discord_reader_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmd = " ".join(proc.info['cmdline']).lower()
                if 'discordreader.py' in cmd:
                    return True
        except:
            pass
    return False



def kill_discord_reader():
    for proc in psutil.process_iter(['pid','name','cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmd = " ".join(proc.info['cmdline']).lower()
                if 'discordreader.py' in cmd:
                    proc.terminate()
        except:
            pass

def log_all_python_processes():
    try:
        with open(r"C:\CeladonListener\monitor_debug.txt","a") as f:
            f.write("=== PROCESS SCAN START ===\n")

            for proc in psutil.process_iter(['pid','name','cmdline']):
                try:
                    name = proc.info['name']
                    cmd = proc.info['cmdline']
                    f.write(f"PID={proc.pid}, NAME={name}, CMD={cmd}\n")

                    # Log the first few memory maps
                    count = 0
                    for m in proc.memory_maps():
                        f.write(f"    MMAP: {m.path}\n")
                        count += 1
                        if count >= 3:
                            break

                    f.write("\n")

                except Exception as e:
                    f.write(f"Error reading process: {e}\n")
            f.write("=== PROCESS SCAN END ===\n")
    except:
        pass

while True:
    log_all_python_processes()

    try:
        with open(r"C:\CeladonListener\monitor_debug.txt","a") as f:
            f.write("Loop tick. KillSwitch=" + str(kill_switch_on()) + "\n")
    except:
        pass

    if kill_switch_on():
        with open(r"C:\CeladonListener\monitor_debug.txt","a") as f:
            f.write("Kill detected. Killing reader.\n")
        kill_discord_reader()
        time.sleep(2)
        continue

    running = is_discord_reader_running()
    with open(r"C:\CeladonListener\monitor_debug.txt","a") as f:
        f.write("ReaderRunning=" + str(running) + "\n")

    if not running:
        with open(r"C:\CeladonListener\monitor_debug.txt","a") as f:
            f.write("Starting discordReader.\n")
        subprocess.Popen([PYTHON_EXE, DISCORD_READER_PATH])
    time.sleep(5)

