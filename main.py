# python3 -m pip install adafruit-circuitpython-dht
import smbus
import time

# I²C slave address of the Elegoo Uno R3
SLAVE_ADDR = 4

# Create an I²C bus object (bus 1 is standard on most Raspberry Pis)
bus = smbus.SMBus(1)

def read_sensor_data():
    try:
        # Arduino slaves typically allow up to 32 bytes per transaction.
        # Adjust the "length" as needed based on your formatted string length.
        num_bytes = 32
        data = bus.read_i2c_block_data(SLAVE_ADDR, 0, num_bytes)
        # Convert the received list of integers into a string.
        sensor_string = ''.join(chr(x) for x in data)
        # Remove any trailing null (0) characters from the string.
        sensor_string = sensor_string.split('\x00')[0]
        return sensor_string
    except Exception as e:
        print("I2C communication error:", e)
        return None

while True:
    sensor_data = read_sensor_data()
    if sensor_data:
        # Expected format: "temperature,pH,EC,water_level"
        print("Sensor Data:", sensor_data)
    else:
        print("Failed to receive data.")
    time.sleep(2)
