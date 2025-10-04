from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class BloomIntensity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class VegetationType(str, Enum):
    FOREST = "forest"
    GRASSLAND = "grassland"
    AGRICULTURAL = "agricultural"
    DESERT = "desert"
    WETLAND = "wetland"
    SHRUBLAND = "shrubland"

class Season(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

class SatelliteSource(str, Enum):
    LANDSAT = "landsat"
    MODIS = "modis"
    VIIRS = "viirs"
    SENTINEL = "sentinel"
    PACE = "pace"
    EMIT = "emit"

class PlantBloomEvent(BaseModel):
    """Model representing a plant blooming event"""
    id: str = Field(..., description="Unique identifier for the bloom event")
    location: str = Field(..., description="Location name or description")
    region: str = Field(..., description="Geographic region")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    detection_date: datetime = Field(..., description="Date when bloom was detected")
    intensity: BloomIntensity = Field(..., description="Bloom intensity level")
    confidence: float = Field(..., ge=0, le=100, description="Detection confidence percentage")
    vegetation_type: VegetationType = Field(..., description="Type of vegetation")
    season: Season = Field(..., description="Season when bloom occurred")
    satellite_source: SatelliteSource = Field(..., description="Satellite that detected the bloom")
    spectral_bands: Dict[str, float] = Field(..., description="Spectral band values")
    area_coverage: float = Field(..., ge=0, description="Area covered by bloom in square kilometers")
    duration_days: int = Field(..., ge=1, description="Expected duration of bloom in days")
    ecological_impact: Optional[str] = Field(None, description="Ecological significance")
    conservation_priority: Optional[int] = Field(None, ge=1, le=5, description="Conservation priority (1-5)")

class SatelliteData(BaseModel):
    """Model representing satellite observation data"""
    satellite: SatelliteSource = Field(..., description="Satellite source")
    acquisition_date: datetime = Field(..., description="Date of satellite acquisition")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    spectral_data: Dict[str, float] = Field(..., description="Spectral band measurements")
    cloud_coverage: float = Field(..., ge=0, le=100, description="Cloud coverage percentage")
    spatial_resolution: float = Field(..., description="Spatial resolution in meters")
    quality_score: float = Field(..., ge=0, le=1, description="Data quality score")

class BloomDetection(BaseModel):
    """Model representing bloom detection results"""
    location: str = Field(..., description="Detection location")
    coordinates: List[float] = Field(..., description="[longitude, latitude] coordinates")
    bloom_probability: float = Field(..., ge=0, le=1, description="Probability of bloom occurrence")
    intensity_score: float = Field(..., ge=0, le=1, description="Bloom intensity score")
    vegetation_index: float = Field(..., description="Vegetation index value")
    anomaly_score: float = Field(..., description="Anomaly detection score")
    temporal_trend: str = Field(..., description="Temporal trend description")
    recommended_actions: List[str] = Field(..., description="Recommended conservation actions")

class GlobalStatistics(BaseModel):
    """Model for global bloom statistics"""
    total_events: int = Field(..., description="Total number of bloom events")
    events_by_region: Dict[str, int] = Field(..., description="Events count by region")
    events_by_season: Dict[str, int] = Field(..., description="Events count by season")
    events_by_intensity: Dict[str, int] = Field(..., description="Events count by intensity")
    average_confidence: float = Field(..., description="Average detection confidence")
    most_active_regions: List[str] = Field(..., description="Most active regions")
    conservation_priorities: List[Dict[str, Any]] = Field(..., description="High priority conservation areas")

class HeatmapData(BaseModel):
    """Model for heatmap visualization data"""
    coordinates: List[List[float]] = Field(..., description="List of [longitude, latitude] coordinates")
    intensities: List[float] = Field(..., description="Bloom intensity values")
    colors: List[str] = Field(..., description="Color values for visualization")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata for visualization")

class FilterParameters(BaseModel):
    """Model for filtering bloom events"""
    region: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    intensity: Optional[BloomIntensity] = None
    vegetation_type: Optional[VegetationType] = None
    satellite_source: Optional[SatelliteSource] = None
    min_confidence: Optional[float] = None
    max_confidence: Optional[float] = None
