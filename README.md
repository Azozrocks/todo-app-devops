# Todo App — My First DevOps Project

A simple REST API built with Python & Flask, containerized with Docker and deployed on Kubernetes.

## Tech Stack
- Python & Flask — REST API
- Docker — Containerization
- Kubernetes (Minikube) — Deployment & Orchestration

## How to Run Locally

### 1. Run with Python
pip install -r requirements.txt
python app.py

### 2. Run with Docker
docker build -t todo-app:v1 .
docker run -p 5000:5000 todo-app:v1

### 3. Deploy on Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service todo-app-service --url

## Docker Image
docker pull azozrocks/todo-app:v1

## API Endpoints
| Method | Endpoint  | Description       |
|--------|-----------|-------------------|
| GET    | /health   | Health check      |
| GET    | /todos    | Get all todos     |
| POST   | /todos    | Add a new todo    |
