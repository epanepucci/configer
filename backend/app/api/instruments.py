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
    instrument_id: str, redis: RedisService = Depends(get_redis_service)
):
    """Get a specific instrument"""
    instrument_data = await redis.get_instrument(instrument_id)
    if not instrument_data:
        raise HTTPException(status_code=404, detail="Instrument not found")

    return Instrument(id=instrument_id, **instrument_data)


@router.post("/", response_model=Instrument)
async def create_instrument(
    instrument: InstrumentCreate, redis: RedisService = Depends(get_redis_service)
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
        "last_updated": None,
    }

    # Add to Redis
    await redis.add_instrument(instrument.id, metadata)

    return Instrument(id=instrument.id, **metadata)
