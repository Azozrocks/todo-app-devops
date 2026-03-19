import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def make_todo(id=1, task="Test task", done=False):
    return {"id": id, "task": task, "done": done}


@patch("app.get_db")
def test_health(mock_db, client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


@patch("app.get_db")
def test_home(mock_db, client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["version"] == "2.0"


@patch("app.get_db")
def test_get_todos(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = [make_todo(1, "Task 1"), make_todo(2, "Task 2")]

    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


@patch("app.get_db")
def test_get_todo_by_id(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = make_todo(1, "Test task")

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


@patch("app.get_db")
def test_get_todo_not_found(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = None

    response = client.get("/todos/999")
    assert response.status_code == 404


@patch("app.get_db")
def test_add_todo(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = make_todo(1, "New task")

    response = client.post("/todos", json={"task": "New task"})
    assert response.status_code == 201
    assert response.get_json()["task"] == "New task"


@patch("app.get_db")
def test_add_todo_missing_task(mock_db, client):
    response = client.post("/todos", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


@patch("app.get_db")
def test_update_todo(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.side_effect = [
        make_todo(1, "Old task", False),
        make_todo(1, "New task", True)
    ]

    response = client.put("/todos/1", json={"task": "New task", "done": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data["task"] == "New task"
    assert data["done"] == True


@patch("app.get_db")
def test_update_todo_not_found(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = None

    response = client.put("/todos/999", json={"task": "Ghost"})
    assert response.status_code == 404


@patch("app.get_db")
def test_delete_todo(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = make_todo(1, "To be deleted")

    response = client.delete("/todos/1")
    assert response.status_code == 200


@patch("app.get_db")
def test_delete_todo_not_found(mock_db, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = None

    response = client.delete("/todos/999")
    assert response.status_code == 404