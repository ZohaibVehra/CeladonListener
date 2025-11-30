import os
import time
import sys

# testkill.txt lives next to this script
LOCAL_FILE_PATH = os.path.join(os.path.dirname(__file__), "testkill.txt")

# kill.txt lives in shared folder — CHANGE THIS PATH
KILL_FILE_PATH = r"Z:\kill.txt"   # adjust if needed


def ensure_file():
    if not os.path.exists(LOCAL_FILE_PATH):
        with open(LOCAL_FILE_PATH, "w") as f:
            f.write("1")
        print("Created testkill.txt with value 1.")
    else:
        print("testkill.txt already exists.")


def read_number():
    with open(LOCAL_FILE_PATH, "r") as f:
        content = f.read().strip()
    try:
        return int(content)
    except ValueError:
        print("Invalid content found, resetting to 1.")
        return 1


def write_number(num):
    with open(LOCAL_FILE_PATH, "w") as f:
        f.write(str(num))


def read_kill_flag():
    """Read kill.txt to see if script should terminate."""
    try:
        with open(KILL_FILE_PATH, "r") as f:
            return f.read().strip().lower()
    except:
        return "run"  # default if missing


def main():
    ensure_file()

    start = time.time()
    DURATION = 300  # 5 minutes

    while time.time() - start < DURATION:

        # 🔥 check kill flag every loop
        kill_flag = read_kill_flag()
        if kill_flag == "kill":
            print("Kill flag detected. Exiting cleanly...")
            sys.exit(0)  # NSSM will NOT restart

        current = read_number()
        new_val = current + 1
        write_number(new_val)

        print(f"Updated value: {new_val}")

        time.sleep(10)

    print("Done. 5 minutes passed.")
    sys.exit(0)  # also exit normally


if __name__ == "__main__":
    main()
