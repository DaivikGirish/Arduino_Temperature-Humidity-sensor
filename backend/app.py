from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
import datetime
import certifi
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import logging

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/iot_db')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "IoT Sensor API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# MongoDB Connection
try:
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    client.admin.command('ping')  # Test connection
    db = client['iot']
    collection = db['temperature']
    print("Connected to MongoDB")
except errors.ServerSelectionTimeoutError as e:
    print("MongoDB connection failed:", e)
    collection = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/api/temperature/add', methods=['POST'])
def add_temperature():
    data = request.get_json()
    logger.info('Received data: %s', data)
    # Strict input validation
    if not isinstance(data, dict):
        logger.warning('Invalid data type: %s', data)
        return jsonify({'error': 'Invalid data format'}), 400
    allowed_fields = {'temperature', 'humidity', 'timestamp'}
    if not allowed_fields.issuperset(data.keys()):
        logger.warning('Extra fields in data: %s', data)
        return jsonify({'error': 'Unexpected fields in input'}), 400
    try:
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        if not (-50 <= temperature <= 150):
            return jsonify({'error': 'Temperature out of range'}), 400
        if not (0 <= humidity <= 100):
            return jsonify({'error': 'Humidity out of range'}), 400
    except (KeyError, ValueError, TypeError):
        logger.warning('Invalid temperature or humidity value: %s', data)
        return jsonify({'error': 'Invalid temperature or humidity value'}), 400
    # Timestamp validation
    if 'timestamp' in data:
        try:
            data['timestamp'] = datetime.datetime.fromisoformat(data['timestamp'].replace("Z", "+00:00"))
        except ValueError:
            return jsonify({'error': 'Invalid timestamp format'}), 400
    else:
        data['timestamp'] = datetime.datetime.now(datetime.timezone.utc)
    # Insert into MongoDB
    if collection is None:
        print("MongoDB not connected.")
        return jsonify({"error": "Database not connected"}), 500
    try:
        result = collection.insert_one(data)
        print("Inserted document ID:", result.inserted_id)
        return jsonify({"message": "Data inserted", "inserted_id": str(result.inserted_id)}), 201
    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": "Server error", "details": str(e)}), 500


@app.route('/api/temperature/all', methods=['GET'])
def get_all_data():
    if collection is None:
        return jsonify({"error": "Database not connected"}), 500

    try:
        docs = list(collection.find())
        for doc in docs:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string for JSON
        return jsonify(docs)
    except Exception as e:
        print("Error fetching documents:", e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/status', methods=['GET'])
def db_status():
    try:
        client.admin.command('ping')
        return jsonify({"status": "Connected to MongoDB"}), 200
    except Exception as e:
        return jsonify({"status": "Disconnected", "error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Try a simple DB operation if collection is available
        if collection:
            collection.estimated_document_count()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        logger.error('Health check failed: %s', e)
        return jsonify({'status': 'error', 'details': str(e)}), 500


# Run the server and make it network-accessible
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
