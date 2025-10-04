"""
Plant Database Module for BloomTracker Plant Sensor Analysis System.

This module contains the plant knowledge base with optimal growing conditions,
care requirements, and troubleshooting information for different plant types.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PlantDatabase:
    """Database containing plant information and optimal growing conditions."""
    
    def __init__(self):
        self.plants = self._load_plant_data()
    
    def _load_plant_data(self) -> Dict[str, Dict[str, Any]]:
        """Load plant data from JSON schemas."""
        return {
            "chili_pepper": {
                "name": "Chili Pepper",
                "scientific_name": "Capsicum annuum",
                "category": "Vegetable",
                "growth_stages": {
                    "germination": {
                        "duration_days": "7-14",
                        "temperature": {"min": 20, "max": 30, "optimal": 25},
                        "humidity": {"min": 70, "max": 90, "optimal": 80},
                        "soil_moisture": {"min": 60, "max": 80, "optimal": 70},
                        "light_intensity": {"min": 200, "max": 400, "optimal": 300},
                        "soil_ph": {"min": 6.0, "max": 7.0, "optimal": 6.5}
                    },
                    "vegetative": {
                        "duration_days": "30-60",
                        "temperature": {"min": 18, "max": 28, "optimal": 23},
                        "humidity": {"min": 60, "max": 80, "optimal": 70},
                        "soil_moisture": {"min": 50, "max": 70, "optimal": 60},
                        "light_intensity": {"min": 400, "max": 800, "optimal": 600},
                        "soil_ph": {"min": 6.0, "max": 7.0, "optimal": 6.5}
                    },
                    "flowering": {
                        "duration_days": "14-21",
                        "temperature": {"min": 20, "max": 26, "optimal": 23},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 50, "max": 70, "optimal": 60},
                        "light_intensity": {"min": 600, "max": 1000, "optimal": 800},
                        "soil_ph": {"min": 6.0, "max": 7.0, "optimal": 6.5}
                    },
                    "fruiting": {
                        "duration_days": "30-60",
                        "temperature": {"min": 18, "max": 26, "optimal": 22},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 60, "max": 80, "optimal": 70},
                        "light_intensity": {"min": 600, "max": 1000, "optimal": 800},
                        "soil_ph": {"min": 6.0, "max": 7.0, "optimal": 6.5}
                    }
                },
                "care_requirements": {
                    "watering": "Keep soil consistently moist but not waterlogged",
                    "fertilizing": "Use balanced fertilizer every 2-3 weeks during growing season",
                    "pruning": "Remove lower leaves and suckers to improve air circulation",
                    "pest_control": "Watch for aphids, spider mites, and whiteflies"
                },
                "common_issues": {
                    "yellow_leaves": "Usually indicates overwatering or nutrient deficiency",
                    "dropping_flowers": "Often caused by high temperatures or insufficient pollination",
                    "small_fruits": "May be due to insufficient light or nutrients",
                    "wilting": "Check for root rot or underwatering"
                },
                "harvesting": {
                    "timing": "Harvest when fruits reach desired size and color",
                    "frequency": "Pick regularly to encourage more fruit production",
                    "storage": "Store in cool, dry place or refrigerate for longer shelf life"
                }
            },
            
            "grapevine": {
                "name": "Grapevine",
                "scientific_name": "Vitis vinifera",
                "category": "Fruit",
                "growth_stages": {
                    "dormancy": {
                        "duration_days": "90-120",
                        "temperature": {"min": -5, "max": 10, "optimal": 2},
                        "humidity": {"min": 40, "max": 60, "optimal": 50},
                        "soil_moisture": {"min": 30, "max": 50, "optimal": 40},
                        "light_intensity": {"min": 0, "max": 200, "optimal": 100},
                        "soil_ph": {"min": 6.0, "max": 7.5, "optimal": 6.8}
                    },
                    "bud_break": {
                        "duration_days": "14-21",
                        "temperature": {"min": 10, "max": 20, "optimal": 15},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 300, "max": 600, "optimal": 450},
                        "soil_ph": {"min": 6.0, "max": 7.5, "optimal": 6.8}
                    },
                    "vegetative": {
                        "duration_days": "60-90",
                        "temperature": {"min": 15, "max": 30, "optimal": 22},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.0, "max": 7.5, "optimal": 6.8}
                    },
                    "flowering": {
                        "duration_days": "7-14",
                        "temperature": {"min": 18, "max": 25, "optimal": 21},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.0, "max": 7.5, "optimal": 6.8}
                    },
                    "fruit_development": {
                        "duration_days": "60-90",
                        "temperature": {"min": 20, "max": 30, "optimal": 25},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 50, "max": 70, "optimal": 60},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.0, "max": 7.5, "optimal": 6.8}
                    },
                    "ripening": {
                        "duration_days": "30-45",
                        "temperature": {"min": 18, "max": 28, "optimal": 23},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.0, "max": 7.5, "optimal": 6.8}
                    }
                },
                "care_requirements": {
                    "watering": "Deep watering once or twice per week, more during fruit development",
                    "fertilizing": "Apply balanced fertilizer in spring, potassium-rich in summer",
                    "pruning": "Prune in winter to control growth and improve fruit quality",
                    "pest_control": "Watch for powdery mildew, downy mildew, and grape berry moth"
                },
                "common_issues": {
                    "powdery_mildew": "White powdery coating on leaves, treat with fungicide",
                    "downy_mildew": "Yellow spots on leaves, improve air circulation",
                    "bird_damage": "Use netting to protect ripening grapes",
                    "poor_fruit_set": "May be due to weather during flowering or insufficient pollination"
                },
                "harvesting": {
                    "timing": "Harvest when grapes reach desired sweetness and color",
                    "frequency": "Single harvest per season",
                    "storage": "Store in cool, humid conditions or process into wine/juice"
                }
            },
            
            "olive_tree": {
                "name": "Olive Tree",
                "scientific_name": "Olea europaea",
                "category": "Tree",
                "growth_stages": {
                    "dormancy": {
                        "duration_days": "120-150",
                        "temperature": {"min": -5, "max": 15, "optimal": 8},
                        "humidity": {"min": 40, "max": 60, "optimal": 50},
                        "soil_moisture": {"min": 30, "max": 50, "optimal": 40},
                        "light_intensity": {"min": 200, "max": 600, "optimal": 400},
                        "soil_ph": {"min": 6.5, "max": 8.5, "optimal": 7.5}
                    },
                    "bud_break": {
                        "duration_days": "21-30",
                        "temperature": {"min": 10, "max": 20, "optimal": 15},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 400, "max": 800, "optimal": 600},
                        "soil_ph": {"min": 6.5, "max": 8.5, "optimal": 7.5}
                    },
                    "vegetative": {
                        "duration_days": "90-120",
                        "temperature": {"min": 15, "max": 30, "optimal": 22},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.5, "max": 8.5, "optimal": 7.5}
                    },
                    "flowering": {
                        "duration_days": "14-21",
                        "temperature": {"min": 18, "max": 25, "optimal": 21},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.5, "max": 8.5, "optimal": 7.5}
                    },
                    "fruit_development": {
                        "duration_days": "120-150",
                        "temperature": {"min": 20, "max": 30, "optimal": 25},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 50, "max": 70, "optimal": 60},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.5, "max": 8.5, "optimal": 7.5}
                    },
                    "ripening": {
                        "duration_days": "60-90",
                        "temperature": {"min": 15, "max": 25, "optimal": 20},
                        "humidity": {"min": 50, "max": 70, "optimal": 60},
                        "soil_moisture": {"min": 40, "max": 60, "optimal": 50},
                        "light_intensity": {"min": 600, "max": 1200, "optimal": 900},
                        "soil_ph": {"min": 6.5, "max": 8.5, "optimal": 7.5}
                    }
                },
                "care_requirements": {
                    "watering": "Deep watering every 1-2 weeks, drought tolerant once established",
                    "fertilizing": "Apply balanced fertilizer in spring, avoid high nitrogen",
                    "pruning": "Prune in late winter to maintain shape and improve air circulation",
                    "pest_control": "Watch for olive fruit fly, scale insects, and fungal diseases"
                },
                "common_issues": {
                    "olive_fruit_fly": "Major pest, use traps and organic treatments",
                    "scale_insects": "Small insects on leaves and branches, treat with horticultural oil",
                    "fungal_diseases": "Prevent with good air circulation and proper watering",
                    "poor_fruit_set": "May be due to weather during flowering or insufficient chilling hours"
                },
                "harvesting": {
                    "timing": "Harvest when olives reach desired ripeness (green to black)",
                    "frequency": "Annual harvest in fall",
                    "storage": "Process into oil or cure for table olives"
                }
            }
        }
    
    def get_plant_list(self) -> List[Dict[str, str]]:
        """Get list of all available plants with basic information."""
        return [
            {
                "name": plant_data["name"],
                "scientific_name": plant_data["scientific_name"],
                "category": plant_data["category"],
                "key": plant_key
            }
            for plant_key, plant_data in self.plants.items()
        ]
    
    def get_plant_parameters(self, plant_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed parameters for a specific plant."""
        plant_key = self._get_plant_key(plant_name)
        if plant_key not in self.plants:
            return None
        
        return self.plants[plant_key]
    
    def get_optimal_conditions(self, plant_name: str, growth_stage: str) -> Optional[Dict[str, Any]]:
        """Get optimal conditions for a specific plant and growth stage."""
        plant_data = self.get_plant_parameters(plant_name)
        if not plant_data or growth_stage not in plant_data["growth_stages"]:
            return None
        
        return plant_data["growth_stages"][growth_stage]
    
    def _get_plant_key(self, plant_name: str) -> str:
        """Convert plant name to internal key."""
        name_mapping = {
            "chili pepper": "chili_pepper",
            "chili_peppers": "chili_pepper",
            "pepper": "chili_pepper",
            "grapevine": "grapevine",
            "grape": "grapevine",
            "grapes": "grapevine",
            "olive tree": "olive_tree",
            "olive": "olive_tree",
            "olives": "olive_tree"
        }
        return name_mapping.get(plant_name.lower(), plant_name.lower())
    
    def get_plant_health_indicators(self, plant_name: str, growth_stage: str) -> Dict[str, str]:
        """Get health indicators and recommendations for a plant."""
        plant_data = self.get_plant_parameters(plant_name)
        if not plant_data:
            return {}
        
        return {
            "care_requirements": plant_data["care_requirements"],
            "common_issues": plant_data["common_issues"],
            "harvesting": plant_data["harvesting"]
        }

# Global plant database instance
plant_db = PlantDatabase()
