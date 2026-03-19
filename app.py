import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", 5432),
        dbname=os.environ.get("DB_NAME", "tododb"),
        user=os.environ.get("DB_USER", "todouser"),
        password=os.environ.get("DB_PASSWORD", "todopassword"),
        cursor_factory=RealDictCursor
    )


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def reset_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos")
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    return jsonify({"message": "Welcome to Todo App!", "version": "2.0"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(list(todos))


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    todo = cur.fetchone()
    cur.close()
    conn.close()
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(dict(todo))


@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Field 'task' is required"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO todos (task, done) VALUES (%s, %s) RETURNING *",
        (data["task"], False)
    )
    todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(todo)), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    todo = cur.fetchone()
    if todo is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Todo not found"}), 404
    data = request.get_json()
    task = data.get("task", todo["task"])
    done = data.get("done", todo["done"])
    cur.execute(
        "UPDATE todos SET task = %s, done = %s WHERE id = %s RETURNING *",
        (task, done, todo_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(updated))


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    todo = cur.fetchone()
    if todo is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Todo not found"}), 404
    cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Todo {todo_id} deleted"}), 200


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)