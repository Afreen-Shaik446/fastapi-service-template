# fastapi-service-template

A production-style FastAPI microservice template: health/readiness probes, OpenAPI docs, JWT auth, structured JSON logging, environment-based config, multi-stage Docker build, Kubernetes manifests, and a GitHub Actions CI pipeline with pytest.

This is a template for demonstration purposes — it shows patterns, not a production deployment.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Run locally
export APP_JWT_SECRET="dev-secret-change-me"
uvicorn app.main:app --reload

# Docs: http://localhost:8000/docs
# Health: http://localhost:8000/healthz
```

## Authenticated example

```bash
# Mint a token (demo helper, not for production use)
python - <<'EOF'
from app.deps import create_access_token
from app.config import get_settings
print(create_access_token("demo-user", get_settings()))
EOF

TOKEN=<paste-token>
curl -X POST localhost:8000/items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "widget", "description": "demo item"}'
```

## Tests

```bash
pytest -v
```

## Docker

```bash
docker build -t fastapi-service-template:local .
docker run -p 8000:8000 -e APP_JWT_SECRET="dev-secret-change-me" fastapi-service-template:local
```

## Kubernetes

Manifests live in `k8s/`. Replace the placeholder host in `ingress.yaml` before applying.

```bash
kubectl apply -f k8s/
```

## Configuration

All settings are environment variables prefixed with `APP_`:

| Variable | Default | Description |
|---|---|---|
| `APP_ENVIRONMENT` | `development` | Environment name (used in logs) |
| `APP_LOG_LEVEL` | `INFO` | Logging level |
| `APP_JWT_SECRET` | `change-me-in-production` | HS256 signing secret — **must** be set in real deployments (use ≥32 random bytes) |
| `APP_JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `APP_JWT_EXPIRE_MINUTES` | `60` | Token lifetime |
