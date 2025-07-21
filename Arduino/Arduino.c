// Run this code in Arduino IDE
#include <DHT.h>

// Define the DHT sensor
#define DHTPIN 2          // DHT22 data pin connected to Arduino digital pin 2
#define DHTTYPE DHT22     // Change to DHT11 if using DHT11 sensor

DHT dht(DHTPIN, DHTTYPE);

// Setup
void setup() {
  Serial.begin(9600);   // Start Serial communication
  dht.begin();          // Initialize the DHT sensor
  delay(2000);          // Give time for sensor to stabilize

  Serial.println("[Arduino] Starting...");
}

// Main loop
void loop() {
  // Reading temperature or humidity takes about 250ms!
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();  // Default is Celsius

  // Check if any reads failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("[Arduino] Failed to read from DHT sensor!");
  } else {
    // Format: temperature,humidity
    Serial.print(temperature, 1);
    Serial.print(",");
    Serial.println(humidity, 1);
  }

  delay(5000);  // Send data every 5 seconds
}