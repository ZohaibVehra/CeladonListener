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

'''
we are always going to check the most recent message
we will also have a state variable, Recent, which is false

when we hit, we confirm its false and change it to true and do w.e else we need to do
then, whenever the newest post anything but virtual queue, we will change it back to false

this allows us to not notify on the same virtual queue message through multiple checks

the assumption is that after every virtual queue post there will be one with product info
'''

KILL_FILE_PATH = r"Z:\kill.txt"   # shared kill-switch file

def kill_switch_on():
    try:
        with open(KILL_FILE_PATH, "r") as f:
            return f.read().strip().lower() == "kill"
    except:
        return False

LAST_VIRTUAL = False
SALE_PATH = r"C:\CeladonListener\FlaskServer\sale.txt" #path to file
load_dotenv()
# os.getenv("API_KEY") usage example


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
    #for test 

    pya.hotkey('ctrl', 'c')
    pya.press('enter')
    time.sleep(.2)
    return pyperclip.paste()

#run once initialization is done
def loop():
    global LAST_VIRTUAL
    if kill_switch_on():
        print("Kill flag detected. Exiting discordReader cleanly...")
        sys.exit(0)
    scroll_bottom()
    text = read_latest()
    print(f'latest copy is {text}')
    if 'batman' in text or 'Batman' in text:
        if not LAST_VIRTUAL:
            updateSaletxt(text)
        LAST_VIRTUAL = True
    else:
        LAST_VIRTUAL = False #reset we can now find virtual queue and trigger again


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
    
    # Tool windows don't show in the taskbar
    if win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOOLWINDOW:
        return False
    
    # If it's an app window, WS_EX_APPWINDOW will be set
    if win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_APPWINDOW:
        return True
    
    # If it's owned by another window (like popup child windows), skip it
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

#check if discord is running
def is_running():
    for proc in psutil.process_iter(['name']):
        name = proc.info.get('name', '').lower()
        if "discord" in name:
            return True
    return False

#opens discord and navigates to server, to be used through check and initalize func below
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
    

#checks if discord is open and visible, if not corrects
def check_and_initialize():
    if not is_running():
        openDiscord(8)

    if not is_discord_visible():
        openDiscord(2)


#this is what we run, note it will handle initialize
def run():
    if kill_switch_on():
        print("Kill flag detected before start. Exiting cleanly...")
        sys.exit(0)
    start = time.time()  # record start time once

    for i in range(60*12): #3 min
        elapsed = time.time() - start
        print(f"{elapsed:.2f} seconds since start ( discord check {i})")
        check_and_initialize()

        for j in range(24): #24 = roughly 1 min
            if kill_switch_on():
                print("Kill flag detected during message check. Exiting cleanly...")
                sys.exit(0)
            elapsed = time.time() - start
            print(f"{elapsed:.2f} seconds since start (big L {i} text read {j})")
            loop()
            time.sleep(2)


time.sleep(2)

run()
   


