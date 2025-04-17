from flask import Flask, jsonify
from flask_cors import CORS
import serial
import threading
import time

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

SERIAL_PORT = "COM3"
BAUD_RATE = 9600

messages = []

def read_serial():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT}")
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    messages.append(line)
                time.sleep(0.1)
    except Exception as e:
        print(f"Serial error: {e}")

# Start serial thread
threading.Thread(target=read_serial, daemon=True).start()

@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(messages[-100:])  # send last 100 messages

if __name__ == "__main__":
    app.run(debug=True)
