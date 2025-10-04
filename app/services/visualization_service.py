import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from typing import Dict, List, Optional, Any, Tuple
import json
from datetime import datetime

from app.models.plant_models import HeatmapData, PlantBloomEvent, BloomIntensity

class VisualizationService:
    """Service for generating visualizations of bloom data"""
    
    def __init__(self):
        self.color_maps = {
            "bloom_intensity": plt.cm.RdYlGn,
            "confidence": plt.cm.Blues,
            "temporal": plt.cm.viridis
        }
    
    async def generate_bloom_heatmap(
        self, 
        region: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> HeatmapData:
        """Generate bloom intensity heatmap data"""
        # This would typically load real data from a database
        # For now, we'll generate sample heatmap data
        
        # Generate grid of coordinates
        if region == "North America":
            lat_range = (25, 70)
            lon_range = (-170, -50)
        elif region == "Europe":
            lat_range = (35, 70)
            lon_range = (-25, 45)
        elif region == "Asia":
            lat_range = (5, 70)
            lon_range = (60, 180)
        else:  # Global
            lat_range = (-60, 80)
            lon_range = (-180, 180)
        
        # Create grid
        lat_points = np.linspace(lat_range[0], lat_range[1], 20)
        lon_points = np.linspace(lon_range[0], lon_range[1], 30)
        
        coordinates = []
        intensities = []
        colors = []
        
        for lat in lat_points:
            for lon in lon_points:
                coordinates.append([lon, lat])
                
                # Generate realistic bloom intensity based on location and season
                intensity = self._calculate_bloom_intensity(lat, lon, start_date, end_date)
                intensities.append(intensity)
                
                # Convert intensity to color
                color = self._intensity_to_color(intensity)
                colors.append(color)
        
        return HeatmapData(
            coordinates=coordinates,
            intensities=intensities,
            colors=colors,
            metadata={
                "region": region or "Global",
                "start_date": start_date,
                "end_date": end_date,
                "total_points": len(coordinates),
                "max_intensity": max(intensities),
                "min_intensity": min(intensities)
            }
        )
    
    def _calculate_bloom_intensity(self, lat: float, lon: float, start_date: Optional[str], end_date: Optional[str]) -> float:
        """Calculate bloom intensity for a location"""
        # Simulate realistic bloom patterns
        
        # Seasonal factor
        if start_date:
            month = datetime.fromisoformat(start_date).month
            seasonal_factor = self._get_seasonal_bloom_factor(month, lat)
        else:
            seasonal_factor = 0.5
        
        # Geographic factors
        lat_factor = 1.0 - abs(lat) / 90.0  # Higher intensity near equator
        continental_factor = self._get_continental_factor(lat, lon)
        
        # Random variation
        random_factor = np.random.uniform(0.7, 1.3)
        
        # Combine factors
        intensity = seasonal_factor * lat_factor * continental_factor * random_factor
        return max(0.0, min(1.0, intensity))
    
    def _get_seasonal_bloom_factor(self, month: int, lat: float) -> float:
        """Get seasonal bloom factor based on month and latitude"""
        # Northern hemisphere
        if lat > 0:
            if month in [3, 4, 5]:  # Spring
                return 0.9
            elif month in [6, 7, 8]:  # Summer
                return 1.0
            elif month in [9, 10, 11]:  # Autumn
                return 0.6
            else:  # Winter
                return 0.3
        # Southern hemisphere
        else:
            if month in [9, 10, 11]:  # Spring
                return 0.9
            elif month in [12, 1, 2]:  # Summer
                return 1.0
            elif month in [3, 4, 5]:  # Autumn
                return 0.6
            else:  # Winter
                return 0.3
    
    def _get_continental_factor(self, lat: float, lon: float) -> float:
        """Get continental factor for bloom intensity"""
        # Simplified continental patterns
        if 20 <= lat <= 50 and -130 <= lon <= -60:  # North America
            return 0.8
        elif 35 <= lat <= 70 and -25 <= lon <= 45:  # Europe
            return 0.7
        elif 5 <= lat <= 70 and 60 <= lon <= 180:  # Asia
            return 0.9
        elif -35 <= lat <= 5 and 110 <= lon <= 180:  # Australia
            return 0.6
        elif -60 <= lat <= 15 and -90 <= lon <= -30:  # South America
            return 0.8
        else:
            return 0.5
    
    def _intensity_to_color(self, intensity: float) -> str:
        """Convert intensity value to hex color"""
        if intensity < 0.3:
            return "#2E8B57"  # Low intensity - dark green
        elif intensity < 0.6:
            return "#FFD700"  # Medium intensity - gold
        else:
            return "#FF4500"  # High intensity - orange-red
    
    async def generate_temporal_analysis(
        self, 
        lat: float, 
        lon: float, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        """Generate temporal analysis of bloom patterns"""
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        # Generate time series data
        dates = []
        bloom_intensities = []
        vegetation_indices = []
        
        current_date = start_dt
        while current_date <= end_dt:
            dates.append(current_date.isoformat())
            
            # Calculate bloom intensity for this date
            intensity = self._calculate_bloom_intensity(lat, lon, current_date.isoformat(), None)
            bloom_intensities.append(intensity)
            
            # Calculate vegetation index
            vi = 0.3 + 0.5 * intensity + np.random.normal(0, 0.1)
            vegetation_indices.append(max(0, min(1, vi)))
            
            current_date = current_date.replace(day=min(current_date.day + 7, 28))  # Weekly intervals
        
        # Detect peaks and trends
        peaks = self._detect_peaks(bloom_intensities)
        trend = self._calculate_trend(bloom_intensities)
        
        return {
            "dates": dates,
            "bloom_intensities": bloom_intensities,
            "vegetation_indices": vegetation_indices,
            "peaks": peaks,
            "trend": trend,
            "peak_count": len(peaks),
            "average_intensity": np.mean(bloom_intensities)
        }
    
    def _detect_peaks(self, intensities: List[float]) -> List[Dict[str, Any]]:
        """Detect peak bloom events in time series"""
        peaks = []
        threshold = np.mean(intensities) + np.std(intensities)
        
        for i, intensity in enumerate(intensities):
            if intensity > threshold:
                # Check if it's a local maximum
                if i > 0 and i < len(intensities) - 1:
                    if intensity > intensities[i-1] and intensity > intensities[i+1]:
                        peaks.append({
                            "index": i,
                            "intensity": intensity,
                            "significance": "high" if intensity > threshold * 1.5 else "medium"
                        })
        
        return peaks
    
    def _calculate_trend(self, intensities: List[float]) -> str:
        """Calculate trend in bloom intensities"""
        if len(intensities) < 2:
            return "insufficient_data"
        
        # Simple linear trend calculation
        x = np.arange(len(intensities))
        slope = np.polyfit(x, intensities, 1)[0]
        
        if slope > 0.01:
            return "increasing"
        elif slope < -0.01:
            return "decreasing"
        else:
            return "stable"
    
    async def generate_conservation_priority_map(
        self, 
        events: List[PlantBloomEvent]
    ) -> Dict[str, Any]:
        """Generate conservation priority visualization data"""
        priority_data = []
        
        for event in events:
            if event.conservation_priority:
                priority_data.append({
                    "location": event.location,
                    "coordinates": [event.longitude, event.latitude],
                    "priority": event.conservation_priority,
                    "intensity": event.intensity.value,
                    "area": event.area_coverage,
                    "impact": event.ecological_impact
                })
        
        # Sort by priority
        priority_data.sort(key=lambda x: x["priority"], reverse=True)
        
        return {
            "priority_areas": priority_data,
            "total_priority_areas": len(priority_data),
            "high_priority_count": len([p for p in priority_data if p["priority"] >= 4])
        }
