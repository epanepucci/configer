# backend/app/db/redis_client.py
import json
import uuid
from datetime import datetime
import redis.asyncio as redis
from app.core.config import settings


# Helper function to initialize Redis pool
async def init_redis_pool():
    redis_url = (
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    )

    # Create connection pool
    pool = redis.ConnectionPool.from_url(
        redis_url,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,  # Return strings instead of bytes
    )

    # Create Redis client
    client = redis.Redis.from_pool(pool)

    # Test connection
    try:
        await client.ping()
        print("Connected to Redis")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise

    return client


# Redis service class with JSON operations
class RedisService:
    def __init__(self, redis_client):
        self.redis = redis_client

    # --- Instrument Config Operations ---

    async def get_instruments(self):
        """Get list of all instruments"""
        instruments = await self.redis.json().get("instruments:list")
        return instruments or {}

    async def get_instrument(self, instrument_id):
        """Get specific instrument metadata"""
        instruments = await self.redis.json().get("instruments:list")
        if not instruments:
            return None
        return instruments.get(instrument_id)

    async def add_instrument(self, instrument_id, metadata):
        """Add a new instrument"""
        # Check if instruments list exists, create if not
        if not await self.redis.exists("instruments:list"):
            await self.redis.json().set("instruments:list", "$", {})

        # Add instrument to list
        await self.redis.json().set(f"instruments:list", f"$.{instrument_id}", metadata)

        # Initialize empty config
        await self.redis.json().set(f"instrument:{instrument_id}:config", "$", {})

        # Initialize empty versions and snapshots lists
        await self.redis.json().set(f"instrument:{instrument_id}:versions", "$", [])
        await self.redis.json().set(f"instrument:{instrument_id}:snapshots", "$", [])

        return True

    # --- Configuration Operations ---

    async def get_config(self, instrument_id):
        """Get current configuration for an instrument"""
        config = await self.redis.json().get(f"instrument:{instrument_id}:config")
        return config or {}

    async def update_config(self, instrument_id, config_data, user, comment=""):
        """Update configuration and create a new version"""
        # Get current config for comparison
        current_config = await self.get_config(instrument_id)

        # Create changes dict (diff between old and new)
        changes = {}
        for key, new_value in config_data.items():
            if key in current_config and current_config[key] != new_value:
                changes[key] = {"old": current_config[key], "new": new_value}
            elif key not in current_config:
                changes[key] = {"old": None, "new": new_value}

        # If no changes, don't create a new version
        if not changes:
            return None

        # Update current config
        await self.redis.json().set(
            f"instrument:{instrument_id}:config", "$", config_data
        )

        # Create new version
        version_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        version_data = {
            "version_id": version_id,
            "timestamp": timestamp,
            "user": user,
            "comment": comment,
            "data": config_data,
            "changes": changes,
        }

        # Save version
        await self.redis.json().set(
            f"instrument:{instrument_id}:version:{version_id}", "$", version_data
        )

        # Add to versions list
        await self.redis.json().arrappend(
            f"instrument:{instrument_id}:versions", "$", version_id
        )

        # Update last_updated in instrument metadata
        await self.redis.json().set(
            "instruments:list", f"$.{instrument_id}.last_updated", timestamp
        )

        return version_id

    async def get_versions(self, instrument_id):
        """Get all version IDs for an instrument"""
        versions = await self.redis.json().get(f"instrument:{instrument_id}:versions")
        return versions or []

    async def get_version(self, instrument_id, version_id):
        """Get specific version data"""
        version = await self.redis.json().get(
            f"instrument:{instrument_id}:version:{version_id}"
        )
        return version

    # --- Snapshot Operations ---

    async def create_snapshot(self, instrument_id, snapshot_name, description, user):
        """Create a named snapshot of current configuration"""
        # Get current config
        config = await self.get_config(instrument_id)

        # Get latest version ID
        versions = await self.get_versions(instrument_id)
        version_id = versions[-1] if versions else None

        # Create snapshot
        timestamp = datetime.utcnow().isoformat()

        snapshot_data = {
            "snapshot_name": snapshot_name,
            "timestamp": timestamp,
            "user": user,
            "description": description,
            "version_id": version_id,
            "data": config,
        }

        # Save snapshot
        await self.redis.json().set(
            f"instrument:{instrument_id}:snapshot:{snapshot_name}", "$", snapshot_data
        )

        # Add to snapshots list
        await self.redis.json().arrappend(
            f"instrument:{instrument_id}:snapshots", "$", snapshot_name
        )

        return snapshot_name

    async def get_snapshots(self, instrument_id):
        """Get all snapshot names for an instrument"""
        snapshots = await self.redis.json().get(f"instrument:{instrument_id}:snapshots")
        return snapshots or []

    async def get_snapshot(self, instrument_id, snapshot_name):
        """Get specific snapshot data"""
        snapshot = await self.redis.json().get(
            f"instrument:{instrument_id}:snapshot:{snapshot_name}"
        )
        return snapshot
