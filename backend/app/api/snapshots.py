# backend/app/api/snapshots.py
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from app.models.snapshot import SnapshotCreate, Snapshot
from app.db.redis_client import RedisService

router = APIRouter()

# Dependency to get Redis service
async def get_redis_service(request: Request):
    return RedisService(request.app.state.redis)

@router.post("/{instrument_id}", response_model=Snapshot)
async def create_snapshot(
    instrument_id: str,
    snapshot: SnapshotCreate,
    redis: RedisService = Depends(get_redis_service)
):
    """Create a named snapshot of current configuration"""
    # Check if instrument exists
    instrument = await redis.get_instrument(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    # Check if snapshot name already exists
    snapshots = await redis.get_snapshots(instrument_id)
    if snapshot.name in snapshots:
        raise HTTPException(status_code=400, detail="Snapshot name already exists")
    
    # For now, we'll use a hardcoded user (in a real app, get from auth)
    user = "admin"
    
    # Create snapshot
    await redis.create_snapshot(
        instrument_id,
        snapshot.name,
        snapshot.description,
        user
    )
    
    # Get created snapshot
    created_snapshot = await redis.get_snapshot(instrument_id, snapshot.name)
    
    return created_snapshot

@router.get("/{instrument_id}", response_model=List[str])
async def get_snapshots(
    instrument_id: str,
    redis: RedisService = Depends(get_redis_service)
):
    """Get all snapshot names for an instrument"""
    # Check if instrument exists
    instrument = await redis.get_instrument(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    snapshots = await redis.get_snapshots(instrument_id)
    return snapshots

@router.get("/{instrument_id}/{snapshot_name}", response_model=Snapshot)
async def get_snapshot(
    instrument_id: str,
    snapshot_name: str,
    redis: RedisService = Depends(get_redis_service)
):
    """Get specific snapshot data"""
    # Check if instrument exists
    instrument = await redis.get_instrument(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    snapshot = await redis.get_snapshot(instrument_id, snapshot_name)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    
    return snapshot
