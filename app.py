from flask import Flask, jsonify, request

app = Flask(__name__)
todos = []

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def app_todo():
    data = request.get_json()
    todos.append({"id": len(todos) + 1, "task": data["task"]})
    return jsonify(todos[-1]), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Todo App!", "version": "2.0"})    