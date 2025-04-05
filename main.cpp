#include <Wire.h>
#include <DHT.h>

#define SLAVE_ADDRESS 4    // I2C slave address for the Uno
#define DHTPIN 2           // Digital pin for the DHT sensor
#define DHTTYPE DHT11      // Change to DHT22 if needed

DHT dht(DHTPIN, DHTTYPE);

// Analog sensor pin assignments
const int pH_pin = A0;       // pH sensor (analog output)
const int ec_pin = A1;       // EC/TDS sensor (analog output)
const int waterLevel_pin = A2;  // Water level sensor (analog output)

// Global variables updated in the loop (make these volatile if needed)
float last_temp = 0.0;
float last_pH = 0.0;
float last_ec = 0.0;
float last_water_level = 0.0;

void setup() {
  Wire.begin(SLAVE_ADDRESS);     // Join the I2C bus as slave with the given address
  Wire.onRequest(requestEvent);  // Register event for when data is requested by the master

  Serial.begin(9600);    // Optional: for debugging via the serial monitor
  dht.begin();
}

void loop() {
  // Update temperature using the DHT sensor
  float temp = dht.readTemperature();
  if (!isnan(temp)) {
    last_temp = temp;
  } else {
    Serial.println("Error reading temperature sensor!");
  }
  
  // Read and convert the pH sensor data
  int pH_raw = analogRead(pH_pin);
  float pH_voltage = pH_raw * (5.0 / 1023.0);
  // Example conversion factor; calibrate using standard pH buffer solutions!
  last_pH = pH_voltage * 3.5;
  
  // Read and convert the EC/TDS sensor data
  int ec_raw = analogRead(ec_pin);
  float ec_voltage = ec_raw * (5.0 / 1023.0);
  // Example conversion; calibrate using known conductivity solutions.
  last_ec = ec_voltage * 100;
  
  // Read and scale the water level sensor data to a percentage (0–100%)
  int water_raw = analogRead(waterLevel_pin);
  last_water_level = (water_raw / 1023.0) * 100.0;
  
  delay(2000);  // Update sensor readings every 2 seconds
}

// This function is automatically called when the Raspberry Pi requests sensor data.
void requestEvent() {
  // Format the sensor readings into a comma-separated string with 2-decimal precision.
  char buf[50];
  snprintf(buf, sizeof(buf), "%.2f,%.2f,%.2f,%.2f", last_temp, last_pH, last_ec, last_water_level);
  Wire.write(buf);   // Send the sensor string over I²C to the master.
}
