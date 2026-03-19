import pytest
from app import app, reset_todos

@pytest.fixture
def client():
    reset_todos()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["version"] == "2.0"


def test_get_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_todo(client):
    response = client.post("/todos", json={"task": "Learn Github Actions"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["task"] == "Learn Github Actions"
    assert data["done"] == False
    assert data["id"] == 1


def test_add_todo_missing_task(client):
    response = client.post("/todos", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_todo_by_id(client):
    client.post("/todos", json={"task": "Test todo"})
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_update_todo(client):
    client.post("/todos", json={"task": "Old task"})
    response = client.put("/todos/1", json={"task": "New task", "done": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data["task"] == "New task"
    assert data["done"] == True


def test_update_todo_not_found(client):
    response = client.put("/todos/999", json={"task": "Ghost"})
    assert response.status_code == 404


def test_delete_todo(client):
    client.post("/todos", json={"task": "To be deleted"})
    response = client.delete("/todos/1")
    assert response.status_code == 200
    # confirm it's gone
    response = client.get("/todos/1")
    assert response.status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404