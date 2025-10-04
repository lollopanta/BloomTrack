import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Configuration
    app_name: str = Field(default="BloomTrack", alias="PROJECT_NAME")
    version: str = Field(default="1.0.0", alias="VERSION")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    secret_key: str = Field(default="your_secret_key_here", alias="SECRET_KEY")
    
    # API Configuration
    api_v1_str: str = Field(default="/api", alias="API_V1_STR")
    allowed_origins: List[str] = Field(default=["http://localhost:3000", "http://localhost:8000"], alias="ALLOWED_ORIGINS")
    
    # NASA API Configuration
    nasa_api_key: str = Field(default="demo_key", alias="NASA_API_KEY")
    nasa_earth_data_url: str = Field(default="https://earthengine.googleapis.com/v1alpha", alias="NASA_EARTH_DATA_URL")
    nasa_laads_daac_url: str = Field(default="https://ladsweb.modaps.eosdis.nasa.gov/api/v2", alias="NASA_LAADS_DAAC_URL")
    nasa_gibs_url: str = Field(default="https://gibs.earthdata.nasa.gov/wmts/1.0.0/WMTSCapabilities.xml", alias="NASA_GIBS_URL")
    
    # NASA Data Collections
    landsat_collection: str = Field(default="LANDSAT/LC08/C02/T1_L2", alias="LANDSAT_COLLECTION")
    modis_collection: str = Field(default="MOD09GA", alias="MODIS_COLLECTION")
    viirs_collection: str = Field(default="NOAA/VIIRS/001/VNP09GA", alias="VIIRS_COLLECTION")
    sentinel_collection: str = Field(default="COPERNICUS/S2_SR", alias="SENTINEL_COLLECTION")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./bloomtrack.db", alias="DATABASE_URL")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="bloomtrack", alias="DB_NAME")
    db_user: str = Field(default="username", alias="DB_USER")
    db_password: str = Field(default="password", alias="DB_PASSWORD")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    
    # Data Processing Configuration
    max_workers: int = Field(default=4, alias="MAX_WORKERS")
    cache_ttl: int = Field(default=3600, alias="CACHE_TTL")
    batch_size: int = Field(default=100, alias="BATCH_SIZE")
    data_refresh_interval: int = Field(default=3600, alias="DATA_REFRESH_INTERVAL")
    
    # Geospatial Configuration
    default_map_center_lat: float = Field(default=20.0, alias="DEFAULT_MAP_CENTER_LAT")
    default_map_center_lon: float = Field(default=0.0, alias="DEFAULT_MAP_CENTER_LON")
    default_zoom_level: int = Field(default=2, alias="DEFAULT_ZOOM_LEVEL")
    spatial_resolution: int = Field(default=30, alias="SPATIAL_RESOLUTION")
    
    # Machine Learning Configuration
    ml_model_path: str = Field(default="./models", alias="ML_MODEL_PATH")
    training_data_path: str = Field(default="./data/training", alias="TRAINING_DATA_PATH")
    prediction_confidence_threshold: float = Field(default=0.7, alias="PREDICTION_CONFIDENCE_THRESHOLD")
    
    # Export Configuration
    export_formats: List[str] = Field(default=["geojson", "csv", "kml", "shp"], alias="EXPORT_FORMATS")
    max_export_records: int = Field(default=10000, alias="MAX_EXPORT_RECORDS")
    
    class Config:
        env_file = "config.env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings

def load_env_file(env_file: str = "config.env") -> None:
    """Load environment variables from file"""
    env_path = Path(env_file)
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
