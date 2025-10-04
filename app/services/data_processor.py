import pandas as pd
import geopandas as gpd
import numpy as np
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import os
from shapely.geometry import Point
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from app.models.plant_models import (
    PlantBloomEvent, BloomDetection, GlobalStatistics, 
    BloomIntensity, VegetationType, Season, SatelliteSource
)

class DataProcessor:
    """Service for processing plant blooming data and detecting bloom events"""
    
    def __init__(self):
        self.sample_data = self._load_sample_data()
    
    def _load_sample_data(self) -> List[PlantBloomEvent]:
        """Load sample bloom event data"""
        sample_events = [
            PlantBloomEvent(
                id="bloom_001",
                location="California Central Valley",
                region="North America",
                latitude=36.7783,
                longitude=-119.4179,
                detection_date=datetime(2024, 3, 15),
                intensity=BloomIntensity.HIGH,
                confidence=92.5,
                vegetation_type=VegetationType.AGRICULTURAL,
                season=Season.SPRING,
                satellite_source=SatelliteSource.LANDSAT,
                spectral_bands={"NDVI": 0.78, "EVI": 0.65, "SAVI": 0.72},
                area_coverage=1250.5,
                duration_days=45,
                ecological_impact="Critical for pollinator support and crop yield",
                conservation_priority=4
            ),
            PlantBloomEvent(
                id="bloom_002",
                location="Amazon Rainforest",
                region="South America",
                latitude=-3.4653,
                longitude=-62.2159,
                detection_date=datetime(2024, 2, 28),
                intensity=BloomIntensity.MEDIUM,
                confidence=87.3,
                vegetation_type=VegetationType.FOREST,
                season=Season.SPRING,
                satellite_source=SatelliteSource.MODIS,
                spectral_bands={"NDVI": 0.82, "EVI": 0.71, "SAVI": 0.79},
                area_coverage=8500.2,
                duration_days=60,
                ecological_impact="Essential for tropical ecosystem biodiversity",
                conservation_priority=5
            ),
            PlantBloomEvent(
                id="bloom_003",
                location="Sahara Desert Oasis",
                region="Africa",
                latitude=23.4241,
                longitude=25.6969,
                detection_date=datetime(2024, 4, 2),
                intensity=BloomIntensity.LOW,
                confidence=75.8,
                vegetation_type=VegetationType.DESERT,
                season=Season.SPRING,
                satellite_source=SatelliteSource.VIIRS,
                spectral_bands={"NDVI": 0.45, "EVI": 0.38, "SAVI": 0.42},
                area_coverage=125.8,
                duration_days=15,
                ecological_impact="Rare desert bloom event supporting local wildlife",
                conservation_priority=3
            ),
            PlantBloomEvent(
                id="bloom_004",
                location="Australian Outback",
                region="Oceania",
                latitude=-25.2744,
                longitude=133.7751,
                detection_date=datetime(2024, 3, 22),
                intensity=BloomIntensity.HIGH,
                confidence=89.1,
                vegetation_type=VegetationType.SHRUBLAND,
                season=Season.AUTUMN,
                satellite_source=SatelliteSource.SENTINEL,
                spectral_bands={"NDVI": 0.71, "EVI": 0.58, "SAVI": 0.67},
                area_coverage=3200.7,
                duration_days=30,
                ecological_impact="Post-fire recovery bloom supporting ecosystem regeneration",
                conservation_priority=4
            ),
            PlantBloomEvent(
                id="bloom_005",
                location="Siberian Tundra",
                region="Asia",
                latitude=61.5240,
                longitude=105.3188,
                detection_date=datetime(2024, 6, 10),
                intensity=BloomIntensity.MEDIUM,
                confidence=81.4,
                vegetation_type=VegetationType.GRASSLAND,
                season=Season.SUMMER,
                satellite_source=SatelliteSource.MODIS,
                spectral_bands={"NDVI": 0.68, "EVI": 0.52, "SAVI": 0.61},
                area_coverage=1800.3,
                duration_days=25,
                ecological_impact="Arctic bloom supporting migratory bird populations",
                conservation_priority=3
            )
        ]
        return sample_events
    
    async def get_bloom_events(
        self,
        region: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        intensity: Optional[str] = None
    ) -> List[PlantBloomEvent]:
        """Get bloom events with optional filtering"""
        events = self.sample_data.copy()
        
        # Apply filters
        if region:
            events = [e for e in events if e.region.lower() == region.lower()]
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date)
            events = [e for e in events if e.detection_date >= start_dt]
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date)
            events = [e for e in events if e.detection_date <= end_dt]
        
        if intensity:
            events = [e for e in events if e.intensity.value == intensity.lower()]
        
        return events
    
    async def detect_bloom_events(
        self, 
        lat: float, 
        lon: float, 
        radius: float = 10.0
    ) -> List[BloomDetection]:
        """Detect bloom events in a specific area using geospatial analysis"""
        # Create a point for the search location
        search_point = Point(lon, lat)
        
        # Find events within radius (simplified - in real implementation would use proper geospatial queries)
        nearby_events = []
        for event in self.sample_data:
            event_point = Point(event.longitude, event.latitude)
            distance = search_point.distance(event_point) * 111  # Rough conversion to km
            if distance <= radius:
                nearby_events.append(event)
        
        # Generate detection results
        detections = []
        for event in nearby_events:
            detection = BloomDetection(
                location=event.location,
                coordinates=[event.longitude, event.latitude],
                bloom_probability=event.confidence / 100.0,
                intensity_score=self._calculate_intensity_score(event.intensity),
                vegetation_index=event.spectral_bands.get("NDVI", 0.5),
                anomaly_score=self._calculate_anomaly_score(event),
                temporal_trend=self._analyze_temporal_trend(event),
                recommended_actions=self._generate_recommendations(event)
            )
            detections.append(detection)
        
        return detections
    
    def _calculate_intensity_score(self, intensity: BloomIntensity) -> float:
        """Calculate intensity score from bloom intensity"""
        intensity_map = {
            BloomIntensity.LOW: 0.3,
            BloomIntensity.MEDIUM: 0.6,
            BloomIntensity.HIGH: 0.9
        }
        return intensity_map.get(intensity, 0.5)
    
    def _calculate_anomaly_score(self, event: PlantBloomEvent) -> float:
        """Calculate anomaly score based on event characteristics"""
        # Simplified anomaly calculation
        base_score = 0.5
        if event.vegetation_type == VegetationType.DESERT and event.intensity == BloomIntensity.HIGH:
            base_score += 0.3  # Desert blooms are more anomalous
        if event.area_coverage > 5000:
            base_score += 0.2  # Large area blooms
        return min(base_score, 1.0)
    
    def _analyze_temporal_trend(self, event: PlantBloomEvent) -> str:
        """Analyze temporal trend for the event"""
        if event.season == Season.SPRING:
            return "Expected seasonal bloom"
        elif event.season == Season.AUTUMN and event.vegetation_type == VegetationType.DESERT:
            return "Unusual desert bloom timing"
        else:
            return "Normal seasonal pattern"
    
    def _generate_recommendations(self, event: PlantBloomEvent) -> List[str]:
        """Generate conservation recommendations based on event"""
        recommendations = []
        
        if event.conservation_priority >= 4:
            recommendations.append("High conservation priority - monitor closely")
        
        if event.vegetation_type == VegetationType.FOREST:
            recommendations.append("Protect from deforestation activities")
        
        if event.ecological_impact and "pollinator" in event.ecological_impact.lower():
            recommendations.append("Support pollinator habitat conservation")
        
        if event.area_coverage > 1000:
            recommendations.append("Large-scale bloom - coordinate regional monitoring")
        
        return recommendations
    
    async def get_global_statistics(self) -> GlobalStatistics:
        """Get global bloom statistics"""
        events = self.sample_data
        
        # Calculate statistics
        total_events = len(events)
        
        events_by_region = {}
        events_by_season = {}
        events_by_intensity = {}
        confidence_scores = []
        
        for event in events:
            # Region statistics
            region = event.region
            events_by_region[region] = events_by_region.get(region, 0) + 1
            
            # Season statistics
            season = event.season.value
            events_by_season[season] = events_by_season.get(season, 0) + 1
            
            # Intensity statistics
            intensity = event.intensity.value
            events_by_intensity[intensity] = events_by_intensity.get(intensity, 0) + 1
            
            # Confidence scores
            confidence_scores.append(event.confidence)
        
        # Find most active regions
        most_active_regions = sorted(
            events_by_region.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        most_active_regions = [region for region, _ in most_active_regions]
        
        # Find conservation priorities
        conservation_priorities = []
        for event in events:
            if event.conservation_priority and event.conservation_priority >= 4:
                conservation_priorities.append({
                    "location": event.location,
                    "priority": event.conservation_priority,
                    "impact": event.ecological_impact,
                    "area": event.area_coverage
                })
        
        return GlobalStatistics(
            total_events=total_events,
            events_by_region=events_by_region,
            events_by_season=events_by_season,
            events_by_intensity=events_by_intensity,
            average_confidence=np.mean(confidence_scores),
            most_active_regions=most_active_regions,
            conservation_priorities=conservation_priorities
        )
