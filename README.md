# IoT Temperature & Humidity Sensor

## Overview
This project collects temperature and humidity data using a DHT22 sensor connected to an Arduino. Data is sent via a Python bridge to a Flask backend, which validates and stores it in MongoDB. The project is fully containerized and includes automated testing and API documentation.

## Architecture
- **Arduino**: Reads DHT22 sensor and sends data over serial.
- **Python Bridge**: Reads serial data and POSTs to Flask API.
- **Flask Backend**: Validates, stores, and serves data via REST API.
- **MongoDB**: Stores sensor data.

## Directory Structure
```
IOT-temp-sensor/
├── Arduino/           # Arduino code & Python bridge
├── backend/           # Flask backend, API, tests, Dockerfile
├── database/          # MongoDB init script
├── docker-compose.yml # Orchestrates backend & MongoDB
├── .gitignore         # Ignores venv, pycache, etc.
├── LICENSE            # MIT License
└── README.md          # Project documentation
```

## Quick Start
### 1. Arduino & Sensor
- Wire DHT22 to Arduino and upload `Arduino/Arduino.c`.

### 2. Python Bridge
- Install Python 3.
- Run: `python Arduino/Python-Bridge.py`

### 3. Flask Backend (Local)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python app.py
```

### 4. Docker (Recommended)
```bash
docker-compose up --build
```
- Flask API: [http://localhost:8080](http://localhost:8080)
- MongoDB: `mongodb://localhost:27017`

## API Documentation
- Swagger UI: [http://localhost:8080/api/docs](http://localhost:8080/api/docs)

## Testing
- Backend: `PYTHONPATH=backend pytest backend/tests/`
- Python Bridge: `python -m unittest Arduino/test_python_bridge.py`

## Security & Validation
- Strict input validation and security headers in backend.
- Only essential files are tracked in git.

## Maintenance
- To update dependencies: `pip install --upgrade -r requirements.txt`
- To clean: `find . -type d -name '__pycache__' -exec rm -rf {} +`

## License
MIT License. See `LICENSE` for details. 