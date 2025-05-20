# backend/app/models/instrument.py
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime


class InstrumentBase(BaseModel):
    """Base model for instrument data"""

    name: str = Field(..., description="Instrument name")
    type: str = Field(..., description="Instrument type")
    location: Optional[str] = Field(None, description="Instrument location")


class InstrumentCreate(InstrumentBase):
    """Model for creating an instrument"""

    id: str = Field(..., description="Instrument ID")


class Instrument(InstrumentBase):
    """Model for instrument data with metadata"""

    id: str
    last_updated: Optional[datetime] = None


class InstrumentList(BaseModel):
    """Response model for instrument list"""

    instruments: List[Instrument]
