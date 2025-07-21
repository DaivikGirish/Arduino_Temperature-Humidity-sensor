import serial
import requests
import time
import sys

# Configuration
SERIAL_PORT = 'COM8'  # <-- Change this to your Arduino's serial port (eg. 'COM4' or '/dev/ttyUSB0')
BAUD_RATE = 9600 
SERVER_URL = 'http://192.168.1.135:8080/api/temperature/add'  # <-- Change to your Flask server IP and port


# Attempt to open serial connection
def open_serial():
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
            print(f"Serial connection established on {SERIAL_PORT} at {BAUD_RATE} baud")
            return ser
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            print("Retrying in 2 seconds...")
            time.sleep(2)


def main():
    ser = open_serial()

    while True:
        try:
            # Read a line from Serial
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue

            print(f"📦 Received Serial Data: {line}")

            try:
                # Parse the data
                temp_str, hum_str = line.split(',')
                temperature = float(temp_str)
                humidity = float(hum_str)

                # Prepare payload
                payload = {
                    "temperature": temperature,
                    "humidity": humidity
                }

                # Send POST request
                response = requests.post(SERVER_URL, json=payload, timeout=5)
                print(f"Sent to server: {response.status_code} {response.reason}")

                if response.status_code != 201:
                    print(f"⚠️ Server responded with error: {response.text}")

            except ValueError as ve:
                print(f"Error parsing sensor data: {ve}")
            except requests.exceptions.RequestException as re:
                print(f"HTTP Request failed: {re}")

        except serial.SerialException:
            print("Serial disconnected. Reconnecting...")
            ser.close()
            ser = open_serial()
        except KeyboardInterrupt:
            print("\nStopping bridge...")
            ser.close()
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()