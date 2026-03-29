# Todo App — DevOps Project

A REST API built with Python & Flask, containerized with Docker, and deployed on Kubernetes with a full CI/CD pipeline.

## Tech Stack

- Python & Flask — REST API
- PostgreSQL — Persistent storage
- Docker — Containerization
- Kubernetes (DOKS) — Deployment & Orchestration
- GitHub Actions — CI/CD pipeline
- DigitalOcean — Cloud provider

## Architecture
```
GitHub Push → GitHub Actions (test → build → deploy) → DigitalOcean Kubernetes → PostgreSQL
```

## CI/CD Pipeline

Every push to `main` automatically:
1. Runs tests
2. Builds and pushes a Docker image to Docker Hub
3. Deploys the new image to the Kubernetes cluster

## API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | /health | Health check |
| GET | /todos | Get all todos |
| GET | /todos/\<id\> | Get a single todo |
| POST | /todos | Add a new todo |
| PUT | /todos/\<id\> | Update a todo |
| DELETE | /todos/\<id\> | Delete a todo |

## Monitoring

Uptime Kuma monitors the app's endpoints every 60 seconds and tracks uptime history.

| Monitor | URL |
|---------|-----|
| Health Check | `http://129.212.193.236/health` |
| Todos API | `http://129.212.193.236/todos` |

Uptime Kuma dashboard: `http://64.225.93.70`

## Observability

| Tool | Purpose |
|------|---------|
| Uptime Kuma | External uptime monitoring, endpoint availability |
| Prometheus | Internal metrics collection from cluster and pods |
| Grafana | Metrics visualization and dashboards |

Prometheus and Grafana are deployed via Helm using the `kube-prometheus-stack` chart into the `monitoring` namespace.


## How to Run Locally

### 1. Run with Python
```bash
pip install -r requirements.txt
python app.py
```

### 2. Run with Docker
```bash
docker build -t todo-app .
docker run -p 5000:5000 todo-app
```

### 3. Deploy on Kubernetes
```bash
kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Docker Image
```bash
docker pull azozrocks/todo-app:latest
```