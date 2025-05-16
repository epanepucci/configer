# backend/app/models/config.py
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime

class ConfigBase(BaseModel):
    """Base model for configuration data"""
    data: Dict[str, Any] = Field(..., description="Configuration data")

class ConfigUpdate(ConfigBase):
    """Model for updating configuration"""
    comment: Optional[str] = Field("", description="Comment for this change")

class ConfigVersion(BaseModel):
    """Model for configuration version"""
    version_id: str
    timestamp: datetime
    user: str
    comment: str
    data: Dict[str, Any]
    changes: Dict[str, Dict[str, Any]]

class ConfigVersionResponse(BaseModel):
    """Response model for version list"""
    versions: List[ConfigVersion]

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
