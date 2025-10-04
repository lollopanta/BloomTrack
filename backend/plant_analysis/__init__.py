"""
Plant Analysis Module for BloomTracker Plant Sensor Analysis System.

This module provides comprehensive plant sensor data analysis, AI-powered
gardening advice, and real-time sensor data simulation capabilities.
"""

from .plant_database import PlantDatabase, plant_db
from .plant_advisor import PlantAdvisor, plant_advisor, HealthStatus, SensorReading, PlantAnalysis
from .plant_router import router

__all__ = [
    "PlantDatabase",
    "PlantAdvisor", 
    "HealthStatus",
    "SensorReading",
    "PlantAnalysis",
    "plant_db",
    "plant_advisor",
    "router"
]

__version__ = "1.0.0"
__author__ = "BloomTracker Team"
__description__ = "Plant Sensor Analysis & Advisor System"
