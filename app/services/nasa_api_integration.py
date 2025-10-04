import os
import requests
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum

from app.models.plant_models import PlantBloomEvent, SatelliteData, SatelliteSource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NASADataSource(Enum):
    LANDSAT = "landsat"
    MODIS = "modis"
    VIIRS = "viirs"
    SENTINEL = "sentinel"
    PACE = "pace"
    EMIT = "emit"

@dataclass
class NASAConfig:
    """Configuration for NASA API integration"""
    api_key: str
    earth_data_url: str
    laads_daac_url: str
    gibs_url: str
    landsat_collection: str
    modis_collection: str
    viirs_collection: str
    sentinel_collection: str
    spatial_resolution: int
    cache_ttl: int

class NASAAPIIntegration:
    """Comprehensive NASA API integration for Earth observation data"""
    
    def __init__(self):
        self.config = self._load_config()
        self.session = None
        self.cache = {}
        self.cache_timestamps = {}
    
    def _load_config(self) -> NASAConfig:
        """Load configuration from environment variables"""
        return NASAConfig(
            api_key=os.getenv("NASA_API_KEY", "demo_key"),
            earth_data_url=os.getenv("NASA_EARTH_DATA_URL", "https://earthengine.googleapis.com/v1alpha"),
            laads_daac_url=os.getenv("NASA_LAADS_DAAC_URL", "https://ladsweb.modaps.eosdis.nasa.gov/api/v2"),
            gibs_url=os.getenv("NASA_GIBS_URL", "https://gibs.earthdata.nasa.gov/wmts/1.0.0/WMTSCapabilities.xml"),
            landsat_collection=os.getenv("LANDSAT_COLLECTION", "LANDSAT/LC08/C02/T1_L2"),
            modis_collection=os.getenv("MODIS_COLLECTION", "MOD09GA"),
            viirs_collection=os.getenv("VIIRS_COLLECTION", "NOAA/VIIRS/001/VNP09GA"),
            sentinel_collection=os.getenv("SENTINEL_COLLECTION", "COPERNICUS/S2_SR"),
            spatial_resolution=int(os.getenv("SPATIAL_RESOLUTION", "30")),
            cache_ttl=int(os.getenv("CACHE_TTL", "3600"))
        )
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _get_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate cache key for API requests"""
        return f"{endpoint}_{hash(str(sorted(params.items())))}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache_timestamps:
            return False
        
        cache_time = self.cache_timestamps[cache_key]
        return (datetime.now() - cache_time).seconds < self.config.cache_ttl
    
    async def _make_request(self, url: str, params: Dict[str, Any] = None, 
                          headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Make HTTP request with caching"""
        cache_key = self._get_cache_key(url, params or {})
        
        # Check cache first
        if cache_key in self.cache and self._is_cache_valid(cache_key):
            logger.info(f"Using cached data for {url}")
            return self.cache[cache_key]
        
        # Make API request
        try:
            if self.session:
                async with self.session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Cache the result
                        self.cache[cache_key] = data
                        self.cache_timestamps[cache_key] = datetime.now()
                        
                        return data
                    else:
                        logger.error(f"API request failed: {response.status}")
                        return {"error": f"API request failed with status {response.status}"}
            else:
                # Fallback to requests for synchronous calls
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    self.cache[cache_key] = data
                    self.cache_timestamps[cache_key] = datetime.now()
                    return data
                else:
                    return {"error": f"API request failed with status {response.status_code}"}
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": str(e)}
    
    async def get_landsat_data(self, lat: float, lon: float, 
                             start_date: str, end_date: str) -> List[SatelliteData]:
        """Get Landsat satellite data for a location and time range"""
        try:
            # Simulate Landsat data retrieval (in production, use Google Earth Engine API)
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            satellite_data = []
            current_date = start_dt
            
            while current_date <= end_dt:
                # Simulate Landsat 8 data availability (every 16 days)
                if (current_date - start_dt).days % 16 == 0:
                    # Calculate vegetation indices
                    ndvi = self._calculate_ndvi(lat, lon, current_date)
                    evi = self._calculate_evi(lat, lon, current_date)
                    savi = self._calculate_savi(lat, lon, current_date)
                    
                    data = SatelliteData(
                        satellite=SatelliteSource.LANDSAT,
                        acquisition_date=current_date,
                        latitude=lat,
                        longitude=lon,
                        spectral_data={
                            "NDVI": ndvi,
                            "EVI": evi,
                            "SAVI": savi,
                            "NIR": 0.4 + np.random.normal(0, 0.1),
                            "Red": 0.2 + np.random.normal(0, 0.05),
                            "Green": 0.3 + np.random.normal(0, 0.05),
                            "Blue": 0.25 + np.random.normal(0, 0.05),
                            "SWIR1": 0.3 + np.random.normal(0, 0.1),
                            "SWIR2": 0.25 + np.random.normal(0, 0.1)
                        },
                        cloud_coverage=np.random.uniform(0, 30),
                        spatial_resolution=30.0,
                        quality_score=np.random.uniform(0.7, 1.0)
                    )
                    satellite_data.append(data)
                
                current_date += timedelta(days=1)
            
            return satellite_data
            
        except Exception as e:
            logger.error(f"Error getting Landsat data: {str(e)}")
            return []
    
    async def get_modis_data(self, lat: float, lon: float, 
                           start_date: str, end_date: str) -> List[SatelliteData]:
        """Get MODIS satellite data for a location and time range"""
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            satellite_data = []
            current_date = start_dt
            
            while current_date <= end_dt:
                # MODIS data is available daily
                ndvi = self._calculate_ndvi(lat, lon, current_date)
                evi = self._calculate_evi(lat, lon, current_date)
                
                data = SatelliteData(
                    satellite=SatelliteSource.MODIS,
                    acquisition_date=current_date,
                    latitude=lat,
                    longitude=lon,
                    spectral_data={
                        "NDVI": ndvi,
                        "EVI": evi,
                        "SAVI": self._calculate_savi(lat, lon, current_date),
                        "NIR": 0.4 + np.random.normal(0, 0.1),
                        "Red": 0.2 + np.random.normal(0, 0.05),
                        "Green": 0.3 + np.random.normal(0, 0.05),
                        "Blue": 0.25 + np.random.normal(0, 0.05)
                    },
                    cloud_coverage=np.random.uniform(0, 40),
                    spatial_resolution=250.0,
                    quality_score=np.random.uniform(0.6, 1.0)
                )
                satellite_data.append(data)
                current_date += timedelta(days=1)
            
            return satellite_data
            
        except Exception as e:
            logger.error(f"Error getting MODIS data: {str(e)}")
            return []
    
    async def get_viirs_data(self, lat: float, lon: float, 
                           start_date: str, end_date: str) -> List[SatelliteData]:
        """Get VIIRS satellite data for a location and time range"""
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            satellite_data = []
            current_date = start_dt
            
            while current_date <= end_dt:
                # VIIRS data is available daily
                ndvi = self._calculate_ndvi(lat, lon, current_date)
                
                data = SatelliteData(
                    satellite=SatelliteSource.VIIRS,
                    acquisition_date=current_date,
                    latitude=lat,
                    longitude=lon,
                    spectral_data={
                        "NDVI": ndvi,
                        "EVI": self._calculate_evi(lat, lon, current_date),
                        "SAVI": self._calculate_savi(lat, lon, current_date),
                        "NIR": 0.4 + np.random.normal(0, 0.1),
                        "Red": 0.2 + np.random.normal(0, 0.05),
                        "Green": 0.3 + np.random.normal(0, 0.05),
                        "Blue": 0.25 + np.random.normal(0, 0.05)
                    },
                    cloud_coverage=np.random.uniform(0, 35),
                    spatial_resolution=375.0,
                    quality_score=np.random.uniform(0.6, 1.0)
                )
                satellite_data.append(data)
                current_date += timedelta(days=1)
            
            return satellite_data
            
        except Exception as e:
            logger.error(f"Error getting VIIRS data: {str(e)}")
            return []
    
    def _calculate_ndvi(self, lat: float, lon: float, date: datetime) -> float:
        """Calculate NDVI based on location and season"""
        # Seasonal factor
        month = date.month
        if lat > 0:  # Northern hemisphere
            seasonal_factor = self._get_northern_seasonal_factor(month)
        else:  # Southern hemisphere
            seasonal_factor = self._get_southern_seasonal_factor(month)
        
        # Latitude factor (higher vegetation near equator)
        lat_factor = 1.0 - abs(lat) / 90.0
        
        # Base NDVI calculation
        base_ndvi = 0.3 + 0.4 * seasonal_factor * lat_factor
        
        # Add some noise
        noise = np.random.normal(0, 0.1)
        return max(0.0, min(1.0, base_ndvi + noise))
    
    def _calculate_evi(self, lat: float, lon: float, date: datetime) -> float:
        """Calculate EVI based on NDVI"""
        ndvi = self._calculate_ndvi(lat, lon, date)
        # EVI is typically 0.8-0.9 of NDVI
        return ndvi * 0.85 + np.random.normal(0, 0.05)
    
    def _calculate_savi(self, lat: float, lon: float, date: datetime) -> float:
        """Calculate SAVI (Soil Adjusted Vegetation Index)"""
        ndvi = self._calculate_ndvi(lat, lon, date)
        # SAVI is typically 0.9-1.0 of NDVI
        return ndvi * 0.95 + np.random.normal(0, 0.03)
    
    def _get_northern_seasonal_factor(self, month: int) -> float:
        """Get seasonal factor for Northern Hemisphere"""
        if month in [3, 4, 5]:  # Spring
            return 0.8
        elif month in [6, 7, 8]:  # Summer
            return 1.0
        elif month in [9, 10, 11]:  # Autumn
            return 0.6
        else:  # Winter
            return 0.3
    
    def _get_southern_seasonal_factor(self, month: int) -> float:
        """Get seasonal factor for Southern Hemisphere"""
        if month in [9, 10, 11]:  # Spring
            return 0.8
        elif month in [12, 1, 2]:  # Summer
            return 1.0
        elif month in [3, 4, 5]:  # Autumn
            return 0.6
        else:  # Winter
            return 0.3
    
    async def get_comprehensive_satellite_data(self, lat: float, lon: float, 
                                             start_date: str, end_date: str) -> List[SatelliteData]:
        """Get comprehensive satellite data from multiple sources"""
        all_data = []
        
        # Get data from all sources
        tasks = [
            self.get_landsat_data(lat, lon, start_date, end_date),
            self.get_modis_data(lat, lon, start_date, end_date),
            self.get_viirs_data(lat, lon, start_date, end_date)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                all_data.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Error in satellite data retrieval: {result}")
        
        return all_data
    
    async def detect_bloom_events_from_satellite_data(self, lat: float, lon: float, 
                                                    start_date: str, end_date: str) -> List[PlantBloomEvent]:
        """Detect bloom events from satellite data analysis"""
        try:
            satellite_data = await self.get_comprehensive_satellite_data(lat, lon, start_date, end_date)
            
            if not satellite_data:
                return []
            
            # Group data by date
            data_by_date = {}
            for data in satellite_data:
                date_key = data.acquisition_date.date()
                if date_key not in data_by_date:
                    data_by_date[date_key] = []
                data_by_date[date_key].append(data)
            
            bloom_events = []
            
            for date, daily_data in data_by_date.items():
                # Calculate average vegetation indices
                avg_ndvi = np.mean([d.spectral_data.get("NDVI", 0) for d in daily_data])
                avg_evi = np.mean([d.spectral_data.get("EVI", 0) for d in daily_data])
                avg_confidence = np.mean([d.quality_score * 100 for d in daily_data])
                
                # Detect bloom if NDVI is above threshold
                if avg_ndvi > 0.6:  # High vegetation activity
                    # Determine intensity
                    if avg_ndvi > 0.8:
                        intensity = "high"
                    elif avg_ndvi > 0.7:
                        intensity = "medium"
                    else:
                        intensity = "low"
                    
                    # Determine vegetation type based on location
                    vegetation_type = self._determine_vegetation_type(lat, lon)
                    
                    # Determine season
                    season = self._determine_season(date, lat)
                    
                    bloom_event = PlantBloomEvent(
                        id=f"nasa_bloom_{date.isoformat()}_{lat}_{lon}",
                        location=f"Location {lat:.2f}, {lon:.2f}",
                        region=self._determine_region(lat, lon),
                        latitude=lat,
                        longitude=lon,
                        detection_date=datetime.combine(date, datetime.min.time()),
                        intensity=intensity,
                        confidence=avg_confidence,
                        vegetation_type=vegetation_type,
                        season=season,
                        satellite_source=SatelliteSource.LANDSAT,  # Primary source
                        spectral_bands={
                            "NDVI": avg_ndvi,
                            "EVI": avg_evi,
                            "SAVI": avg_ndvi * 0.95
                        },
                        area_coverage=100.0,  # Default area
                        duration_days=30,  # Default duration
                        ecological_impact="Detected via satellite analysis",
                        conservation_priority=3 if intensity == "high" else 2
                    )
                    
                    bloom_events.append(bloom_event)
            
            return bloom_events
            
        except Exception as e:
            logger.error(f"Error detecting bloom events: {str(e)}")
            return []
    
    def _determine_vegetation_type(self, lat: float, lon: float) -> str:
        """Determine vegetation type based on location"""
        # Simplified vegetation type determination
        if lat > 60 or lat < -60:  # Polar regions
            return "grassland"
        elif abs(lat) < 30:  # Tropical/subtropical
            if lon > -30 and lon < 50:  # Africa
                return "grassland"
            elif lon > 60 and lon < 180:  # Asia
                return "forest"
            else:
                return "forest"
        else:  # Temperate regions
            if lon > -130 and lon < -60:  # North America
                return "agricultural"
            elif lon > -30 and lon < 50:  # Europe/Africa
                return "grassland"
            else:
                return "forest"
    
    def _determine_season(self, date: datetime.date, lat: float) -> str:
        """Determine season based on date and latitude"""
        month = date.month
        
        if lat > 0:  # Northern hemisphere
            if month in [3, 4, 5]:
                return "spring"
            elif month in [6, 7, 8]:
                return "summer"
            elif month in [9, 10, 11]:
                return "autumn"
            else:
                return "winter"
        else:  # Southern hemisphere
            if month in [9, 10, 11]:
                return "spring"
            elif month in [12, 1, 2]:
                return "summer"
            elif month in [3, 4, 5]:
                return "autumn"
            else:
                return "winter"
    
    def _determine_region(self, lat: float, lon: float) -> str:
        """Determine geographic region based on coordinates"""
        if lat > 60:
            return "Arctic"
        elif lat < -60:
            return "Antarctic"
        elif lat > 30:
            if lon > -170 and lon < -50:
                return "North America"
            elif lon > -30 and lon < 50:
                return "Europe"
            elif lon > 50 and lon < 180:
                return "Asia"
            else:
                return "North America"
        elif lat < -30:
            if lon > -90 and lon < -30:
                return "South America"
            elif lon > 110 and lon < 180:
                return "Oceania"
            else:
                return "South America"
        else:  # Tropical regions
            if lon > -90 and lon < -30:
                return "South America"
            elif lon > -30 and lon < 50:
                return "Africa"
            elif lon > 50 and lon < 180:
                return "Asia"
            else:
                return "Asia"
    
    async def get_nasa_earth_data_catalog(self) -> Dict[str, Any]:
        """Get NASA Earth Data catalog information"""
        try:
            # This would integrate with NASA's Earth Data catalog
            # For now, return simulated catalog data
            return {
                "collections": {
                    "landsat": {
                        "name": "Landsat 8 Surface Reflectance",
                        "description": "Landsat 8 OLI/TIRS surface reflectance data",
                        "resolution": "30m",
                        "temporal_resolution": "16 days",
                        "bands": ["Blue", "Green", "Red", "NIR", "SWIR1", "SWIR2"]
                    },
                    "modis": {
                        "name": "MODIS Surface Reflectance",
                        "description": "MODIS Terra/Aqua surface reflectance data",
                        "resolution": "250m-1000m",
                        "temporal_resolution": "Daily",
                        "bands": ["Red", "NIR", "Blue", "Green", "SWIR1", "SWIR2"]
                    },
                    "viirs": {
                        "name": "VIIRS Surface Reflectance",
                        "description": "VIIRS Suomi NPP surface reflectance data",
                        "resolution": "375m",
                        "temporal_resolution": "Daily",
                        "bands": ["Red", "NIR", "Blue", "Green"]
                    }
                },
                "last_updated": datetime.now().isoformat(),
                "total_collections": 3
            }
        except Exception as e:
            logger.error(f"Error getting NASA catalog: {str(e)}")
            return {"error": str(e)}
