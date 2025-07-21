import pytest
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code in (200, 404)  # Adjust based on your actual home route

@patch('app.collection')
def test_add_temperature_success(mock_collection, client):
    mock_collection.insert_one.return_value.inserted_id = '12345'
    payload = {"temperature": 25.0, "humidity": 60.0}
    response = client.post('/api/temperature/add', json=payload)
    assert response.status_code == 201
    assert "inserted_id" in response.get_json()

@patch('app.collection')
def test_add_temperature_missing_fields(mock_collection, client):
    payload = {"temperature": 25.0}
    response = client.post('/api/temperature/add', json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

@patch('app.collection')
def test_get_all_data_success(mock_collection, client):
    mock_collection.find.return_value = [
        {"_id": "1", "temperature": 25.0, "humidity": 60.0, "timestamp": "2024-01-01T00:00:00Z"}
    ]
    response = client.get('/api/temperature/all')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["temperature"] == 25.0

@patch('app.collection')
def test_add_and_get_temperature_integration(mock_collection, client):
    # Simulate insert_one and find for integration
    mock_collection.insert_one.return_value.inserted_id = 'abc123'
    mock_collection.find.return_value = [
        {"_id": "abc123", "temperature": 22.5, "humidity": 55.0, "timestamp": "2024-01-01T00:00:00Z"}
    ]
    # Add data
    payload = {"temperature": 22.5, "humidity": 55.0}
    response = client.post('/api/temperature/add', json=payload)
    assert response.status_code == 201
    # Get all data
    response = client.get('/api/temperature/all')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]["temperature"] == 22.5
    assert data[0]["humidity"] == 55.0 