# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import config, instruments, snapshots
from app.core.config import settings
from app.db.redis_client import init_redis_pool

app = FastAPI(
    title="Configuration Manager API",
    description="API for managing instrument configurations",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(instruments.router, prefix="/api/instruments", tags=["instruments"])
app.include_router(config.router, prefix="/api/configs", tags=["configs"])
app.include_router(snapshots.router, prefix="/api/snapshots", tags=["snapshots"])

@app.on_event("startup")
async def startup_db_client():
    app.state.redis = await init_redis_pool()

@app.on_event("shutdown")
async def shutdown_db_client():
    await app.state.redis.close()

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
