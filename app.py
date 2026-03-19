from flask import Flask, jsonify, request

app = Flask(__name__)
todos = []
next_id = 1


@app.route("/")
def home():
    return jsonify({"message": "Welcome to Todo App!", "version": "2.0"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo)


@app.route("/todos", methods=["POST"])
def add_todo():
    global next_id
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Field 'task' is required"}), 400
    todo = {"id": next_id, "task": data["task"], "done": False}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    data = request.get_json()
    if "task" in data:
        todo["task"] = data["task"]
    if "done" in data:
        todo["done"] = data["done"]
    return jsonify(todo)


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"message": f"Todo {todo_id} deleted"}), 200


def reset_todos():
    global todos, next_id
    todos = []
    next_id = 1


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)