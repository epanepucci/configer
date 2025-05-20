# backend/app/models/snapshot.py
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class SnapshotCreate(BaseModel):
    """Model for creating a snapshot"""

    name: str = Field(..., description="Snapshot name")
    description: Optional[str] = Field("", description="Snapshot description")


class Snapshot(BaseModel):
    """Model for snapshot data"""

    snapshot_name: str
    timestamp: datetime
    user: str
    description: str
    version_id: Optional[str]
    data: Dict[str, Any]


class SnapshotResponse(BaseModel):
    """Response model for snapshot list"""

    snapshots: List[Snapshot]
