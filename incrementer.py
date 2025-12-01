import os
import time
import pyautogui as pya
from datetime import datetime


pya.FAILSAFE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "counter.txt")
FLAG_PATH = r"\\192.168.2.29\VMStuff\kill.txt"

def log_timestamp():
    try:
        with open(LOG_FILE, "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    except Exception as e:
        print("Log error:", e)


def read_flag():
    try:
        with open(FLAG_PATH, "r") as f:
            return f.read().strip().lower()
    except:
        return ""

screen_w, screen_h = pya.size()
offset = 50
positions = [
    (offset, offset),
    (screen_w - offset, offset),
    (screen_w - offset, screen_h - offset),
    (offset, screen_h - offset)
]

def main():
    print("Corner mover + flag monitor started...")
    idx = 0

    while True:
        flag = read_flag()

        if flag == "kill":
            print("Kill flag active — idling...")
            time.sleep(3)
            continue

        log_timestamp()

        x, y = positions[idx]
        idx = (idx + 1) % len(positions)

        pya.moveTo(x, y, duration=0.3)

        time.sleep(5)

if __name__ == "__main__":
    main()
