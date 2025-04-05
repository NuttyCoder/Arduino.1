# python3 -m pip install adafruit-circuitpython-dht
import time
import board
import adafruit_dht

# Set up the sensor (DHT11 here) on GPIO4
dht_sensor = adafruit_dht.DHT11(board.D4)

while True:
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        print(f"Temperature: {temperature}°C   Humidity: {humidity}%")
    except Exception as e:
        print("Error reading DHT sensor:", e)
    time.sleep(2)
