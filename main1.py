import smbus
import time

SLAVE_ADDR = 4
bus = smbus.SMBus(1)

def read_sensor_data():
    # Request data from the slave. Adjust the number of bytes (64 here) based on expected message size.
    num_bytes = 64
    try:
        data = bus.read_i2c_block_data(SLAVE_ADDR, 0, num_bytes)
        sensor_string = ''.join(chr(x) for x in data)
        sensor_string = sensor_string.split('\x00')[0].strip()  # Remove trailing nulls
        return sensor_string
    except Exception as e:
        print("I2C communication error:", e)
        return None

def parse_and_validate(sensor_string):
    # Expected format: "#T:xx.xx,P:xx.xx,E:xx.xx,W:xx.xx,S:x,CS:XX$"
    if not sensor_string.startswith("#") or not sensor_string.endswith("$"):
        print("Invalid message format")
        return None

    # Remove start and end markers
    content = sensor_string[1:-1]
    parts = content.split(',')
    
    # Extract checksum from the parts; also construct a string for checksum recalculation.
    cs_from_msg = None
    message_for_checksum = ""
    for part in parts:
        if part.startswith("CS:"):
            cs_from_msg = part[3:]
        else:
            message_for_checksum += part + ","
    if message_for_checksum.endswith(","):
        message_for_checksum = message_for_checksum[:-1]
        
    # Compute checksum: sum the ASCII values of message_for_checksum and modulo by 256
    checksum_calc = sum(ord(c) for c in message_for_checksum) % 256
    try:
        checksum_msg = int(cs_from_msg, 16)
    except (TypeError, ValueError):
        print("Checksum conversion error")
        return None

    if checksum_calc != checksum_msg:
        print("Checksum mismatch: calculated", hex(checksum_calc), "vs received", cs_from_msg)
        return None

    # Parse sensor values into a dictionary.
    data = {}
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

while True:
    sensor_data = read_sensor_data()
    if sensor_data:
        parsed_data = parse_and_validate(sensor_data)
        if parsed_data:
            print("Sensor Data:", parsed_data)
        else:
            print("Received invalid sensor data:", sensor_data)
    else:
        print("Failed to retrieve sensor data")
    time.sleep(2)
