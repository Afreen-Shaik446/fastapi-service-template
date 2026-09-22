"""Liveness and readiness probes."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", tags=["health"], summary="Liveness probe")
def liveness() -> dict:
    return {"status": "ok"}


@router.get("/readyz", tags=["health"], summary="Readiness probe")
def readiness() -> dict:
    # Extend with real dependency checks (DB, broker) as the service grows.
    return {"status": "ready"}
