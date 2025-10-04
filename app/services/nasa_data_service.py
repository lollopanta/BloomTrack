import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import numpy as np

from app.models.plant_models import SatelliteData, SatelliteSource

class NASADataService:
    """Service for interacting with NASA Earth observation data APIs"""
    
    def __init__(self):
        self.base_urls = {
            "landsat": "https://earthengine.googleapis.com/v1alpha",
            "modis": "https://earthengine.googleapis.com/v1alpha",
            "viirs": "https://earthengine.googleapis.com/v1alpha"
        }
        self.api_key = "demo_key"  # In production, use environment variable
    
    async def get_satellite_data(
        self, 
        lat: float, 
        lon: float, 
        start_date: str, 
        end_date: str
    ) -> List[SatelliteData]:
        """Get satellite data for a specific location and time range"""
        # This is a simplified implementation
        # In a real application, you would integrate with actual NASA APIs
        
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        # Generate sample satellite data
        satellite_data = []
        
        # Simulate different satellite sources
        satellites = [
            SatelliteSource.LANDSAT,
            SatelliteSource.MODIS,
            SatelliteSource.VIIRS
        ]
        
        current_date = start_dt
        while current_date <= end_dt:
            for satellite in satellites:
                # Simulate data availability (not all satellites capture data every day)
                if np.random.random() > 0.3:  # 70% chance of data availability
                    data = SatelliteData(
                        satellite=satellite,
                        acquisition_date=current_date,
                        latitude=lat,
                        longitude=lon,
                        spectral_data=self._generate_spectral_data(lat, lon, current_date),
                        cloud_coverage=np.random.uniform(0, 30),
                        spatial_resolution=self._get_spatial_resolution(satellite),
                        quality_score=np.random.uniform(0.7, 1.0)
                    )
                    satellite_data.append(data)
            
            current_date += timedelta(days=1)
        
        return satellite_data
    
    def _generate_spectral_data(self, lat: float, lon: float, date: datetime) -> Dict[str, float]:
        """Generate realistic spectral data based on location and season"""
        # Simulate seasonal and geographic variations
        season_factor = self._get_seasonal_factor(date)
        lat_factor = abs(lat) / 90.0  # Latitude effect
        
        # Base spectral values
        ndvi = 0.3 + 0.4 * season_factor * (1 - lat_factor * 0.3)
        evi = ndvi * 0.8 + np.random.normal(0, 0.05)
        savi = ndvi * 0.9 + np.random.normal(0, 0.03)
        
        return {
            "NDVI": max(0, min(1, ndvi)),
            "EVI": max(0, min(1, evi)),
            "SAVI": max(0, min(1, savi)),
            "NIR": 0.4 + np.random.normal(0, 0.1),
            "Red": 0.2 + np.random.normal(0, 0.05),
            "Green": 0.3 + np.random.normal(0, 0.05),
            "Blue": 0.25 + np.random.normal(0, 0.05)
        }
    
    def _get_seasonal_factor(self, date: datetime) -> float:
        """Calculate seasonal factor for vegetation growth"""
        # Northern hemisphere seasons
        month = date.month
        if month in [3, 4, 5]:  # Spring
            return 0.8
        elif month in [6, 7, 8]:  # Summer
            return 1.0
        elif month in [9, 10, 11]:  # Autumn
            return 0.6
        else:  # Winter
            return 0.3
    
    def _get_spatial_resolution(self, satellite: SatelliteSource) -> float:
        """Get spatial resolution for different satellites"""
        resolutions = {
            SatelliteSource.LANDSAT: 30.0,
            SatelliteSource.MODIS: 250.0,
            SatelliteSource.VIIRS: 375.0,
            SatelliteSource.SENTINEL: 10.0,
            SatelliteSource.PACE: 1000.0,
            SatelliteSource.EMIT: 60.0
        }
        return resolutions.get(satellite, 30.0)
    
    async def get_vegetation_indices(
        self, 
        lat: float, 
        lon: float, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, List[float]]:
        """Get vegetation indices over time for a location"""
        satellite_data = await self.get_satellite_data(lat, lon, start_date, end_date)
        
        # Group by date and calculate average indices
        indices_by_date = {}
        for data in satellite_data:
            date_key = data.acquisition_date.date()
            if date_key not in indices_by_date:
                indices_by_date[date_key] = []
            indices_by_date[date_key].append(data.spectral_data)
        
        # Calculate time series
        dates = sorted(indices_by_date.keys())
        ndvi_series = []
        evi_series = []
        savi_series = []
        
        for date in dates:
            spectral_data_list = indices_by_date[date]
            avg_ndvi = np.mean([d["NDVI"] for d in spectral_data_list])
            avg_evi = np.mean([d["EVI"] for d in spectral_data_list])
            avg_savi = np.mean([d["SAVI"] for d in spectral_data_list])
            
            ndvi_series.append(avg_ndvi)
            evi_series.append(avg_evi)
            savi_series.append(avg_savi)
        
        return {
            "dates": [d.isoformat() for d in dates],
            "NDVI": ndvi_series,
            "EVI": evi_series,
            "SAVI": savi_series
        }
    
    async def detect_anomalies(
        self, 
        lat: float, 
        lon: float, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        """Detect anomalous vegetation patterns"""
        indices = await self.get_vegetation_indices(lat, lon, start_date, end_date)
        
        # Simple anomaly detection using statistical methods
        ndvi_values = np.array(indices["NDVI"])
        
        # Calculate z-scores
        mean_ndvi = np.mean(ndvi_values)
        std_ndvi = np.std(ndvi_values)
        z_scores = (ndvi_values - mean_ndvi) / std_ndvi if std_ndvi > 0 else np.zeros_like(ndvi_values)
        
        # Identify anomalies (z-score > 2 or < -2)
        anomalies = []
        for i, z_score in enumerate(z_scores):
            if abs(z_score) > 2:
                anomalies.append({
                    "date": indices["dates"][i],
                    "ndvi": ndvi_values[i],
                    "z_score": z_score,
                    "anomaly_type": "high" if z_score > 2 else "low"
                })
        
        return {
            "anomalies": anomalies,
            "mean_ndvi": mean_ndvi,
            "std_ndvi": std_ndvi,
            "anomaly_count": len(anomalies)
        }
