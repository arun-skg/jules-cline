# Deployment Guide

## Docker Compose (Development/Small Scale)
The simplest way to deploy the platform is using Docker Compose.
```bash
docker-compose up -d
```

## Kubernetes (Production Scale)
For enterprise production, use the provided Helm charts (scaffolded in `infra/kubernetes`).

### Prerequisites
- Kubernetes Cluster (EKS, GKE, or local k3s/kind).
- Helm 3.x.
- Managed PostgreSQL, Redis, and Qdrant (recommended).

### Steps
1. **Configure Values:** Update `infra/kubernetes/values.yaml`.
2. **Deploy:**
   ```bash
   helm install enterprise-agent ./infra/kubernetes
   ```

## Horizontal Scaling
- The `api` and `agent-runtime` services are stateless and can be scaled horizontally.
- Use a distributed task queue (Celery/Temporal) for long-running agent tasks.
