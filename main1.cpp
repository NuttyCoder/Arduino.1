#include <Wire.h>
#include <DHT.h>

#define SLAVE_ADDRESS 4    // I²C slave address for the Uno
#define DHTPIN 2           // Digital pin for the DHT sensor
#define DHTTYPE DHT11      // Change this if you are using a DHT22

DHT dht(DHTPIN, DHTTYPE);

// Sensor pin definitions for analog sensors
const int pH_pin = A0;         // pH sensor analog pin
const int ec_pin = A1;         // EC/TDS sensor analog pin
const int waterLevel_pin = A2; // Water level sensor analog pin

// Global variables for sensor values
float last_temp = 0.0;
float last_pH = 0.0;
float last_ec = 0.0;
float last_water_level = 0.0;
bool sensorError = false;  // error flag, true if any sensor reading fails

void setup() {
  Wire.begin(SLAVE_ADDRESS);   // Join I²C bus as slave
  Wire.onRequest(requestEvent); // Register callback for data requests
  Serial.begin(9600);          // For debugging via the serial monitor
  dht.begin();
}

void loop() {
  sensorError = false; // reset error flag on each loop iteration
  
  // ---- Temperature using DHT sensor ----
  float temp = dht.readTemperature();
  if (!isnan(temp)) {
    last_temp = temp;
  } else {
    sensorError = true;
    Serial.println("Error reading temperature sensor!");
  }
  
  // ---- pH Sensor ----
  int pH_raw = analogRead(pH_pin);
  float pH_voltage = pH_raw * (5.0 / 1023.0);
  // Adjust the conversion factor and offset using calibration standards
  last_pH = pH_voltage * 3.5;
  
  // ---- EC/TDS Sensor ----
  int ec_raw = analogRead(ec_pin);
  float ec_voltage = ec_raw * (5.0 / 1023.0);
  // Again, calibrate using known conductivity solutions
  last_ec = ec_voltage * 100;
  
  // ---- Water Level Sensor ----
  int water_raw = analogRead(waterLevel_pin);
  last_water_level = (water_raw / 1023.0) * 100.0;
  
  delay(2000);  // Update sensor values every 2 seconds
}

// This callback is triggered when the Raspberry Pi requests sensor data.
void requestEvent() {
  // Create a structured message:
  // Format: "#T:val,P:val,E:val,W:val,S:flag$" then append ",CS:XX" before the '$'
  char buffer[100];
  snprintf(buffer, sizeof(buffer), "#T:%.2f,P:%.2f,E:%.2f,W:%.2f,S:%d$",
           last_temp, last_pH, last_ec, last_water_level, sensorError ? 1 : 0);
  
  // Calculate a simple checksum (sum of all characters between '#' and '$', modulo 256)
  int len = strlen(buffer);
  int startIndex = 1;       // character after '#'
  int endIndex = len - 1;     // position of '$'
  uint8_t checksum = 0;
  for (int i = startIndex; i < endIndex; i++) {
    checksum += buffer[i];
  }
  
  // Now, rebuild the message with the checksum appended (in hex format) before the '$'
  char message[120];
  // Remove the trailing '$' from the original buffer
  buffer[len - 1] = '\0';
  snprintf(message, sizeof(message), "%s,CS:%02X$", buffer, checksum);
  
  // Send the final message to the master over I²C
  Wire.write(message);
}
