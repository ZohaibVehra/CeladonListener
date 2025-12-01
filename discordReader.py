import sys
from utils import pyUtils as py
from dotenv import load_dotenv
import os
import pyperclip 
import pyautogui as pya
import time
import psutil
import subprocess
import win32gui
import win32con
from datetime import datetime

'''
we are always going to check the most recent message
we will also have a state variable, Recent, which is false

when we hit, we confirm its false and change it to true and do w.e else we need to do
then, whenever the newest post anything but virtual queue, we will change it back to false

this allows us to not notify on the same virtual queue message through multiple checks

the assumption is that after every virtual queue post there will be one with product info
'''

KILL_FILE_PATH = r"\\192.168.2.29\VMStuff\kill.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "counter.txt")

def log_timestamp():
    try:
        with open(LOG_FILE, "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    except Exception as e:
        print("Log error:", e)

def kill_switch_on():
    try:
        with open(KILL_FILE_PATH, "r") as f:
            return f.read().strip().lower() == "kill"
    except:
        return False

LAST_VIRTUAL = False
SALE_PATH = r"C:\CeladonListener\FlaskServer\sale.txt"
load_dotenv()

def scroll_bottom():
    raw = os.getenv("D1_NEWPOST")
    x, y = raw.split(",") 
    x = float(x)
    y = float(y)
    
    py.moveToPercent(x,y)
    py.click()
    py.scrollBottom()

def read_latest():
    raw = os.getenv("D1_NEWPOST")
    x, y = raw.split(",") 
    x = float(x)
    y = float(y)
    
    currx, curry = py.pposition()

    if(abs(x-currx) > 1 or abs(y-curry) > 1):
        print('df')
        py.moveToPercent(x,y)
    time.sleep(.3)
    py.rclick()
    py.press('down')
    time.sleep(0.2)
    py.press('down')

    #for test
    time.sleep(0.2)
    py.press('down')
    time.sleep(0.2)
    py.press('down')
    time.sleep(0.2)
    py.press('down')
    time.sleep(0.2)
    py.press('down')
    time.sleep(0.2)
    py.press('down')
    #for test 

    pya.hotkey('ctrl', 'c')
    pya.press('enter')
    time.sleep(.2)
    return pyperclip.paste()

def loop():
    global LAST_VIRTUAL

    if kill_switch_on():
        print("Kill flag active — DiscordReader idling...")
        time.sleep(3)  # <-- instead of sys.exit(0)
        return

    scroll_bottom()
    text = read_latest()
    log_timestamp()
    print(f'latest copy is {text}')

    if 'batman' in text.lower():
        if not LAST_VIRTUAL:
            updateSaletxt(text)
        LAST_VIRTUAL = True
    else:
        LAST_VIRTUAL = False

def updateSaletxt(text):
    try:
        with open(SALE_PATH, 'w') as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing sale.txt: {e}")

def is_taskbar_window(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False
    if win32gui.GetWindowText(hwnd) == "":
        return False

    if win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOOLWINDOW:
        return False

    if win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_APPWINDOW:
        return True

    if win32gui.GetWindow(hwnd, win32con.GW_OWNER):
        return False

    return True

def is_discord_visible():
    taskbar_windows = []

    def foreach_window(hwnd, _):
        if is_taskbar_window(hwnd):
            title = win32gui.GetWindowText(hwnd)
            taskbar_windows.append((hwnd, title))
        return True

    win32gui.EnumWindows(foreach_window, None)

    for hwnd, title in taskbar_windows:
        if title.split()[-1] == 'Discord':
            if win32gui.IsIconic(hwnd):  
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.2)
                clickServerIcon()
            return True
    return False

def is_running():
    for proc in psutil.process_iter(['name']):
        name = proc.info.get('name', '').lower()
        if "discord" in name:
            return True
    return False

def openDiscord(pause):
    exe = os.getenv("DISCORD_EXE")
    args = os.getenv("DISCORD_ARGS").split()

    print("Launching:", exe, args)
    subprocess.Popen([exe] + args)
    time.sleep(pause)
    clickServerIcon()

def clickServerIcon():
    raw = os.getenv("SEVERICON")
    x, y = raw.split(",") 
    x = float(x)
    y = float(y)
    x,y = py.toAbs(x,y)
    pya.moveTo(x,y)
    time.sleep(.3)
    pya.click()

def check_and_initialize():
    if not is_running():
        openDiscord(8)

    if not is_discord_visible():
        openDiscord(2)

def run():
    #start = time.time()

    for i in range(3):
        if kill_switch_on():
            print("Kill flag active — run() idling...")
            time.sleep(3)  # <-- instead of sys.exit(0)
            continue

        #elapsed = time.time() - start
        #print(f"{elapsed:.2f} seconds since start ( discord check {i})")
        check_and_initialize()

        for j in range(10):
            if kill_switch_on():
                print("Kill flag active — inner loop idling...")
                time.sleep(3)  # <-- instead of sys.exit(0)
                continue

            #elapsed = time.time() - start
            #print(f"{elapsed:.2f} seconds since start (big L {i} text read {j})")
            loop()
            time.sleep(2)

time.sleep(1)
run()