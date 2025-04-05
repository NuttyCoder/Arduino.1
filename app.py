from flask import Flask, jsonify, render_template
import smbus
import time
import threading

app = Flask(__name__)

SLAVE_ADDR = 4
bus = smbus.SMBus(1)
global_sensor_data = {}  # Global variable to hold sensor data

def read_sensor_data():
    num_bytes = 64  # Adjust this as needed
    try:
        data = bus.read_i2c_block_data(SLAVE_ADDR, 0, num_bytes)
        sensor_string = ''.join(chr(x) for x in data)
        sensor_string = sensor_string.split('\x00')[0].strip()
        return sensor_string
    except Exception as e:
        print("I2C communication error:", e)
        return None

def parse_and_validate(sensor_string):
    if not sensor_string.startswith("#") or not sensor_string.endswith("$"):
        return None
    content = sensor_string[1:-1]
    parts = content.split(',')
    data = {}
    cs_from_msg = None
    message_for_checksum = ""
    for part in parts:
        if part.startswith("CS:"):
            cs_from_msg = part[3:]
        else:
            message_for_checksum += part + ","
    if message_for_checksum.endswith(","):
        message_for_checksum = message_for_checksum[:-1]
    checksum_calc = sum(ord(c) for c in message_for_checksum) % 256
    try:
        checksum_msg = int(cs_from_msg, 16)
    except:
        return None
    if checksum_calc != checksum_msg:
        return None
    for part in parts:
        if part.startswith("T:"):
            data["temperature"] = float(part[2:])
        elif part.startswith("P:"):
            data["pH"] = float(part[2:])
        elif part.startswith("E:"):
            data["EC"] = float(part[2:])
        elif part.startswith("W:"):
            data["water_level"] = float(part[2:])
        elif part.startswith("S:"):
            data["status"] = int(part[2:])
    return data

def sensor_polling_thread():
    global global_sensor_data
    while True:
        sensor_str = read_sensor_data()
        if sensor_str:
            parsed = parse_and_validate(sensor_str)
            if parsed:
                global_sensor_data = parsed
        time.sleep(2)

@app.route('/')
def dashboard():
    return render_template("dashboard.html", sensor_data=global_sensor_data)

@app.route('/api/data')
def api_data():
    return jsonify(global_sensor_data)

if __name__ == '__main__':
    # Start sensor polling on a background thread
    t = threading.Thread(target=sensor_polling_thread)
    t.daemon = True
    t.start()
    # Launch the Flask application
    app.run(host='0.0.0.0', port=5000)
