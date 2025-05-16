# backend/app/api/instruments.py
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from app.models.instrument import InstrumentCreate, Instrument, InstrumentList
from app.db.redis_client import RedisService

router = APIRouter()

# Dependency to get Redis service
async def get_redis_service(request: Request):
    return RedisService(request.app.state.redis)

@router.get("/", response_model=InstrumentList)
async def get_instruments(redis: RedisService = Depends(get_redis_service)):
    """Get all instruments"""
    instruments_dict = await redis.get_instruments()
    
    instruments = []
    for id, data in instruments_dict.items():
        instrument = Instrument(id=id, **data)
        instruments.append(instrument)
    
    return {"instruments": instruments}

@router.get("/{instrument_id}", response_model=Instrument)
async def get_instrument(
    instrument_id: str,
    redis: RedisService = Depends(get_redis_service)
):
    """Get a specific instrument"""
    instrument_data = await redis.get_instrument(instrument_id)
    if not instrument_data:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    return Instrument(id=instrument_id, **instrument_data)

@router.post("/", response_model=Instrument)
async def create_instrument(
    instrument: InstrumentCreate,
    redis: RedisService = Depends(get_redis_service)
):
    """Create a new instrument"""
    # Check if instrument already exists
    existing = await redis.get_instrument(instrument.id)
    if existing:
        raise HTTPException(status_code=400, detail="Instrument ID already exists")
    
    # Create metadata object
    metadata = {
        "name": instrument.name,
        "type": instrument.type,
        "location": instrument.location,
        "last_updated": None
    }
    
    # Add to Redis
    await redis.add_instrument(instrument.id, metadata)
    
    return Instrument(id=instrument.id, **metadata)


# backend/app/api/config.py
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Dict, Any, List
from app.models.config import ConfigBase, ConfigUpdate, ConfigVersion, ConfigVersionResponse
from app.db.redis_client import RedisService

router = APIRouter()

# Dependency to get Redis service
async def get_redis_service(request: Request):
    return RedisService(request.app.state.redis)

@router.get("/{instrument_id}", response_model=Dict[str, Any])
async def get_config(
    instrument_id: str,
    redis: RedisService = Depends(get_redis_service)
):
    """Get current configuration for an instrument"""
    # Check if instrument exists
    instrument = await redis.get_instrument(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    config = await redis.get_config(instrument_id)
    return config

@router.put("/{instrument_id}", response_model=Dict[str, Any])
async def update_config(
    instrument_id: str,
    config: ConfigUpdate,
    redis: RedisService = Depends(get_redis_service)
):
    """Update configuration for an instrument"""
    # Check if instrument exists
    instrument = await redis.get_instrument(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    # For now, we'll use a hardcoded user (in a real app, get from auth)
    user = "admin"
    
    # Update config and create version
    version_id = await redis.update_config(
        instrument_id, 
        config.data, 
        user, 
        config.comment
    )
    
    # Get updated config
    updated_config = await redis.get_config(instrument_id)
    
    return {
        "message": "Configuration updated",
        "version_id": version_id,
        "config": updated_config
    }

@router.get("/{instrument_id}/versions", response_model=List[str])
async def get_config_versions(
    instrument_id: str,
    redis: RedisService = Depends(get_redis_service)
):
    """Get all version IDs for an instrument"""
    # Check if instrument exists
    instrument = await redis.get_instrument(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    versions = await redis.get_versions(instrument_id)
    return versions

@router.get("/{instrument_id}/versions/{version_id}", response_model=ConfigVersion)
async def get_config_version(
    instrument_id: str,
    version_id: str,
    redis: RedisService = Depends(get_redis_service)
):
    """Get specific version data"""
    # Check if instrument exists
    instrument = await redis.get_instrument(instrument_id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    version = await redis.get_version(instrument_id, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    return version


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
