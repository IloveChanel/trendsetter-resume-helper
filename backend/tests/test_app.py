import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post("/items/", json={"name": "Item 1", "description": "A test item"})
    assert response.status_code == 201
    assert response.json() == {"name": "Item 1", "description": "A test item"}

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"name": "Item 1", "description": "A test item"}