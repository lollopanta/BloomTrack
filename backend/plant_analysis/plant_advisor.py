"""
Plant Advisor Module for BloomTracker Plant Sensor Analysis System.

This module provides analysis logic, health scoring, and AI integration
for plant sensor data analysis and personalized gardening advice.
"""

import os
import json
import requests
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health status enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class SensorReading:
    """Individual sensor reading with health analysis."""
    parameter: str
    current_value: float
    optimal_min: float
    optimal_max: float
    optimal_target: float
    health_score: float
    status: HealthStatus
    recommendation: str

@dataclass
class PlantAnalysis:
    """Complete plant analysis results."""
    plant_name: str
    growth_stage: str
    overall_health_score: float
    overall_status: HealthStatus
    sensor_readings: List[SensorReading]
    critical_issues: List[str]
    recommendations: List[str]
    ai_advice: Optional[str] = None

class DeepSeekClient:
    """Client for DeepSeek AI API integration."""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.cache = {}  # Simple in-memory cache
    
    def get_gardening_advice(self, plant_data: Dict[str, Any], sensor_data: Dict[str, Any]) -> str:
        """Get personalized gardening advice from DeepSeek AI."""
        if not self.api_key:
            return "AI advice unavailable: DeepSeek API key not configured."
        
        # Create cache key
        cache_key = f"{plant_data['plant_name']}_{json.dumps(sensor_data, sort_keys=True)}"
        
        # Check cache first
        if cache_key in self.cache:
            logger.info("Returning cached AI advice")
            return self.cache[cache_key]
        
        try:
            # Format prompt for gardening advice
            prompt = self._format_gardening_prompt(plant_data, sensor_data)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert horticulturist and plant care specialist. Provide practical, actionable gardening advice based on plant data and sensor readings. Keep responses concise and focused on specific recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            advice = result["choices"][0]["message"]["content"]
            
            # Cache the response
            self.cache[cache_key] = advice
            
            logger.info("Successfully retrieved AI advice from DeepSeek")
            return advice
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            return "AI advice temporarily unavailable. Please try again later."
        except Exception as e:
            logger.error(f"Unexpected error in AI advice: {str(e)}")
            return "AI advice temporarily unavailable. Please try again later."
    
    def _format_gardening_prompt(self, plant_data: Dict[str, Any], sensor_data: Dict[str, Any]) -> str:
        """Format plant data and sensor readings into a prompt for AI advice."""
        prompt = f"""
        Plant: {plant_data['name']} ({plant_data['scientific_name']})
        Growth Stage: {sensor_data['growth_stage']}
        Location: {sensor_data['location']}
        
        Current Sensor Readings:
        - Temperature: {sensor_data['temperature']}°C
        - Humidity: {sensor_data['humidity']}%
        - Soil Moisture: {sensor_data['soil_moisture']}%
        - Light Intensity: {sensor_data['light_intensity']} lux
        - Soil pH: {sensor_data['soil_ph']}
        
        Optimal Conditions for {sensor_data['growth_stage']} stage:
        - Temperature: {plant_data['growth_stages'][sensor_data['growth_stage']]['temperature']['min']}-{plant_data['growth_stages'][sensor_data['growth_stage']]['temperature']['max']}°C
        - Humidity: {plant_data['growth_stages'][sensor_data['growth_stage']]['humidity']['min']}-{plant_data['growth_stages'][sensor_data['growth_stage']]['humidity']['max']}%
        - Soil Moisture: {plant_data['growth_stages'][sensor_data['growth_stage']]['soil_moisture']['min']}-{plant_data['growth_stages'][sensor_data['growth_stage']]['soil_moisture']['max']}%
        - Light Intensity: {plant_data['growth_stages'][sensor_data['growth_stage']]['light_intensity']['min']}-{plant_data['growth_stages'][sensor_data['growth_stage']]['light_intensity']['max']} lux
        - Soil pH: {plant_data['growth_stages'][sensor_data['growth_stage']]['soil_ph']['min']}-{plant_data['growth_stages'][sensor_data['growth_stage']]['soil_ph']['max']}
        
        Please provide specific, actionable advice for optimizing the growing conditions for this plant in its current growth stage.
        """
        return prompt

class PlantAdvisor:
    """Main plant advisor class for sensor data analysis."""
    
    def __init__(self):
        self.deepseek_client = DeepSeekClient()
    
    def analyze_sensor_data(self, sensor_data: Dict[str, Any], plant_name: str) -> PlantAnalysis:
        """Analyze sensor data and provide comprehensive plant health assessment."""
        from .plant_database import plant_db
        
        # Get plant parameters
        plant_data = plant_db.get_plant_parameters(plant_name)
        if not plant_data:
            raise ValueError(f"Plant '{plant_name}' not found in database")
        
        # Get optimal conditions for current growth stage
        optimal_conditions = plant_db.get_optimal_conditions(plant_name, sensor_data['growth_stage'])
        if not optimal_conditions:
            raise ValueError(f"Growth stage '{sensor_data['growth_stage']}' not found for {plant_name}")
        
        # Analyze each sensor parameter
        sensor_readings = []
        critical_issues = []
        recommendations = []
        
        parameters = [
            ('temperature', sensor_data['temperature'], '°C'),
            ('humidity', sensor_data['humidity'], '%'),
            ('soil_moisture', sensor_data['soil_moisture'], '%'),
            ('light_intensity', sensor_data['light_intensity'], 'lux'),
            ('soil_ph', sensor_data['soil_ph'], 'pH')
        ]
        
        for param_name, current_value, unit in parameters:
            reading = self._analyze_parameter(
                param_name, current_value, optimal_conditions[param_name]
            )
            sensor_readings.append(reading)
            
            if reading.status == HealthStatus.CRITICAL:
                critical_issues.append(f"{param_name.title()}: {reading.recommendation}")
            elif reading.status == HealthStatus.WARNING:
                recommendations.append(f"{param_name.title()}: {reading.recommendation}")
        
        # Calculate overall health score
        overall_health_score = sum(reading.health_score for reading in sensor_readings) / len(sensor_readings)
        
        # Determine overall status
        if overall_health_score >= 0.8:
            overall_status = HealthStatus.EXCELLENT
        elif overall_health_score >= 0.6:
            overall_status = HealthStatus.GOOD
        elif overall_health_score >= 0.4:
            overall_status = HealthStatus.WARNING
        else:
            overall_status = HealthStatus.CRITICAL
        
        # Get AI advice
        ai_advice = None
        try:
            ai_advice = self.deepseek_client.get_gardening_advice(plant_data, sensor_data)
        except Exception as e:
            logger.error(f"Error getting AI advice: {str(e)}")
            ai_advice = "AI advice temporarily unavailable."
        
        return PlantAnalysis(
            plant_name=plant_name,
            growth_stage=sensor_data['growth_stage'],
            overall_health_score=overall_health_score,
            overall_status=overall_status,
            sensor_readings=sensor_readings,
            critical_issues=critical_issues,
            recommendations=recommendations,
            ai_advice=ai_advice
        )
    
    def _analyze_parameter(self, param_name: str, current_value: float, optimal_range: Dict[str, float]) -> SensorReading:
        """Analyze a single parameter against optimal range."""
        min_val = optimal_range['min']
        max_val = optimal_range['max']
        target_val = optimal_range['optimal']
        
        # Calculate health score (0-1)
        if min_val <= current_value <= max_val:
            # Within optimal range
            if abs(current_value - target_val) <= (max_val - min_val) * 0.1:
                # Very close to target
                health_score = 1.0
                status = HealthStatus.EXCELLENT
                recommendation = f"Perfect {param_name} level"
            else:
                # Within range but not optimal
                health_score = 0.8
                status = HealthStatus.GOOD
                recommendation = f"Good {param_name} level, could be closer to {target_val}"
        else:
            # Outside optimal range
            if current_value < min_val:
                health_score = max(0, 1 - (min_val - current_value) / (min_val * 0.5))
                status = HealthStatus.CRITICAL if health_score < 0.3 else HealthStatus.WARNING
                recommendation = f"{param_name.title()} too low. Increase to {min_val}-{max_val}"
            else:
                health_score = max(0, 1 - (current_value - max_val) / (max_val * 0.5))
                status = HealthStatus.CRITICAL if health_score < 0.3 else HealthStatus.WARNING
                recommendation = f"{param_name.title()} too high. Decrease to {min_val}-{max_val}"
        
        return SensorReading(
            parameter=param_name,
            current_value=current_value,
            optimal_min=min_val,
            optimal_max=max_val,
            optimal_target=target_val,
            health_score=health_score,
            status=status,
            recommendation=recommendation
        )
    
    def generate_simulated_data(self, plant_name: str, growth_stage: str, location: str = "Indoor") -> Dict[str, Any]:
        """Generate realistic simulated sensor data for testing."""
        from .plant_database import plant_db
        
        plant_data = plant_db.get_plant_parameters(plant_name)
        if not plant_data:
            raise ValueError(f"Plant '{plant_name}' not found in database")
        
        optimal_conditions = plant_db.get_optimal_conditions(plant_name, growth_stage)
        if not optimal_conditions:
            raise ValueError(f"Growth stage '{growth_stage}' not found for {plant_name}")
        
        # Generate realistic sensor data with some variation
        import random
        
        # Add time-based variations
        now = datetime.now()
        hour = now.hour
        
        # Light intensity varies by time of day
        base_light = optimal_conditions['light_intensity']['optimal']
        if 6 <= hour <= 18:  # Daytime
            light_intensity = base_light + random.uniform(-100, 200)
        else:  # Nighttime
            light_intensity = random.uniform(0, 50)
        
        # Temperature varies slightly
        base_temp = optimal_conditions['temperature']['optimal']
        temperature = base_temp + random.uniform(-3, 3)
        
        # Humidity varies
        base_humidity = optimal_conditions['humidity']['optimal']
        humidity = base_humidity + random.uniform(-10, 10)
        
        # Soil moisture varies
        base_moisture = optimal_conditions['soil_moisture']['optimal']
        soil_moisture = base_moisture + random.uniform(-10, 10)
        
        # pH varies slightly
        base_ph = optimal_conditions['soil_ph']['optimal']
        soil_ph = base_ph + random.uniform(-0.3, 0.3)
        
        return {
            "plant_type": plant_name,
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "soil_moisture": round(soil_moisture, 1),
            "light_intensity": round(light_intensity, 0),
            "soil_ph": round(soil_ph, 1),
            "growth_stage": growth_stage,
            "location": location,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_health_status_color(self, status: HealthStatus) -> str:
        """Get color code for health status."""
        color_mapping = {
            HealthStatus.EXCELLENT: "#10B981",  # Green
            HealthStatus.GOOD: "#3B82F6",      # Blue
            HealthStatus.WARNING: "#F59E0B",   # Yellow
            HealthStatus.CRITICAL: "#EF4444"   # Red
        }
        return color_mapping.get(status, "#6B7280")  # Gray as default

# Global plant advisor instance
plant_advisor = PlantAdvisor()
