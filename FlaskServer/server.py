from flask import Flask, jsonify
import os
import datetime
import threading
import time

app = Flask(__name__)

LOG_PING = r"C:\CeladonListener\FlaskServer\serverConsistency.txt"
LOG_ALIVE = r"C:\CeladonListener\FlaskServer\serverConsistencyNoReq.txt"
SALE_PATH = r"C:\CeladonListener\FlaskServer\sale.txt"


def log_ping():
    """Append timestamp to serverConsistency.txt each time endpoint is hit."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PING, "a") as f:
            f.write(f"{timestamp} - ping\n")
    except Exception as e:
        print(f"Logging error (ping): {e}")


def log_alive():
    """Background thread that logs 'alive' every minute."""
    while True:
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_ALIVE, "a") as f:
                f.write(f"{timestamp} - alive\n")
        except Exception as e:
            print(f"Logging error (alive): {e}")
        time.sleep(60)  # every 60 seconds


@app.route('/get-sale', methods=['GET'])
def get_sale():
    try:
        log_ping()

        if not os.path.exists(SALE_PATH):
            print("sale.txt not found.")

        with open(SALE_PATH, 'r') as file:
            content = file.read().strip()

        return jsonify({"sale_status": content}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def start_alive_thread():
    t = threading.Thread(target=log_alive, daemon=True)
    t.start()


if __name__ == "__main__":
    start_alive_thread()
    app.run(debug=False, host="0.0.0.0", port=5000)
