import pytest
from app import app, reset_todos

@pytest.fixture
def client():
    reset_todos()            # reset todos before each test
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_get_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.get_json() == []

def test_add_todo(client):
    response = client.post("/todos",
        json={"task": "Learn Github Actions"}
    )
    assert response.status_code == 201
    assert response.get_json()["task"] == "Learn Github Actions"

    