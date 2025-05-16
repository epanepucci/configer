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
