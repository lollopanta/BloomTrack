"""
Plant AI Advisor Router
Enhanced endpoints for AI-powered plant care advice
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from plant_analysis.deepseek_client import DeepSeekClient

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/plants", tags=["Plant AI Advisor"])

# Initialize DeepSeek client
deepseek_client = DeepSeekClient()

# Plant database (same as existing)
PLANT_DATABASE = {
    "chili_pepper": {
        "name": "Chili Pepper",
        "optimal_conditions": {
            "temperature": {"min": 20, "max": 30, "optimal": 25},
            "humidity": {"min": 40, "max": 70, "optimal": 60},
            "soil_moisture": {"min": 50, "max": 80, "optimal": 65},
            "light_intensity": {"min": 6000, "max": 12000, "optimal": 9000},
            "soil_ph": {"min": 6.0, "max": 7.0, "optimal": 6.5}
        },
        "growth_stages": ["seedling", "vegetative", "flowering", "fruiting"],
        "growing_season": {
            "best_months": ["March", "April", "May", "June", "July", "August", "September"],
            "planting_time": "Early spring (March-April)",
            "harvest_time": "Summer to early fall (July-September)",
            "temperature_range": "20-30°C (68-86°F)",
            "seasonal_notes": "Warm season crop, needs consistent warmth"
        },
        "common_issues": [
            "Yellow leaves (overwatering or nutrient deficiency)",
            "Wilting (underwatering or root rot)",
            "No flowers (insufficient light or nutrients)",
            "Brown spots (fungal infection or sunburn)"
        ]
    },
    "grapevine": {
        "name": "Grapevine",
        "optimal_conditions": {
            "temperature": {"min": 15, "max": 35, "optimal": 25},
            "humidity": {"min": 30, "max": 60, "optimal": 45},
            "soil_moisture": {"min": 40, "max": 70, "optimal": 55},
            "light_intensity": {"min": 8000, "max": 15000, "optimal": 12000},
            "soil_ph": {"min": 6.0, "max": 7.5, "optimal": 6.8}
        },
        "growth_stages": ["dormant", "bud_break", "vegetative", "flowering", "fruit_set", "ripening"],
        "growing_season": {
            "best_months": ["April", "May", "June", "July", "August", "September", "October"],
            "planting_time": "Late winter to early spring (February-March)",
            "harvest_time": "Late summer to early fall (August-October)",
            "temperature_range": "15-35°C (59-95°F)",
            "seasonal_notes": "Perennial vine, dormant in winter, active growing season spring-fall"
        },
        "common_issues": [
            "Powdery mildew (high humidity, poor air circulation)",
            "Black rot (fungal disease, remove affected parts)",
            "Poor fruit set (insufficient pollination or nutrients)",
            "Leaf yellowing (nutrient deficiency or overwatering)"
        ]
    },
    "olive_tree": {
        "name": "Olive Tree",
        "optimal_conditions": {
            "temperature": {"min": 10, "max": 40, "optimal": 25},
            "humidity": {"min": 20, "max": 50, "optimal": 35},
            "soil_moisture": {"min": 30, "max": 60, "optimal": 45},
            "light_intensity": {"min": 10000, "max": 20000, "optimal": 15000},
            "soil_ph": {"min": 6.5, "max": 8.0, "optimal": 7.2}
        },
        "growth_stages": ["dormant", "bud_break", "vegetative", "flowering", "fruit_development"],
        "growing_season": {
            "best_months": ["March", "April", "May", "June", "July", "August", "September", "October"],
            "planting_time": "Early spring (March-April) or fall (September-October)",
            "harvest_time": "Late fall to early winter (October-December)",
            "temperature_range": "10-40°C (50-104°F)",
            "seasonal_notes": "Mediterranean climate tree, drought tolerant, long growing season"
        },
        "common_issues": [
            "Leaf drop (overwatering or temperature stress)",
            "Poor flowering (insufficient light or nutrients)",
            "Fruit drop (water stress or nutrient imbalance)",
            "Scale insects (pest management needed)"
        ]
    }
}

# Request/Response Models
class SensorData(BaseModel):
    temperature: float = Field(..., ge=-10, le=50, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    light_intensity: float = Field(..., ge=0, le=20000, description="Light intensity in lux")
    soil_ph: float = Field(..., ge=4.0, le=9.0, description="Soil pH level")
    growth_stage: str = Field(..., description="Current growth stage")
    location: str = Field(..., description="Indoor or outdoor location")

class ChatMessage(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="Message timestamp")

class PlantAIAnalysisRequest(BaseModel):
    plant_type: str = Field(..., description="Type of plant")
    current_conditions: SensorData = Field(..., description="Current sensor readings")
    user_question: str = Field(..., description="User's gardening question")
    chat_history: List[ChatMessage] = Field(default=[], description="Previous conversation context")

class PlantAIAnalysisResponse(BaseModel):
    success: bool
    advice: str
    health_score: int = Field(..., ge=0, le=100, description="Plant health score (0-100)")
    critical_issues: List[str] = Field(default=[], description="Critical issues identified")
    recommendations: List[str] = Field(default=[], description="Actionable recommendations")
    timestamp: str

class OptimalRangesResponse(BaseModel):
    plant_name: str
    optimal_conditions: Dict[str, Dict[str, float]]
    growth_stages: List[str]
    common_issues: List[str]

class HealthScoreResponse(BaseModel):
    plant_type: str
    health_score: int
    parameter_scores: Dict[str, int]
    critical_issues: List[str]
    recommendations: List[str]

# Utility Functions
def calculate_parameter_score(value: float, optimal_range: Dict[str, float]) -> int:
    """Calculate health score for a single parameter (0-100)"""
    min_val = optimal_range["min"]
    max_val = optimal_range["max"]
    optimal = optimal_range["optimal"]
    
    if min_val <= value <= max_val:
        # Within acceptable range
        distance_from_optimal = abs(value - optimal)
        range_size = max_val - min_val
        score = max(0, 100 - int((distance_from_optimal / (range_size / 2)) * 50))
        return min(100, score)
    else:
        # Outside acceptable range
        if value < min_val:
            distance = min_val - value
        else:
            distance = value - max_val
        return max(0, 50 - int(distance * 10))

def calculate_health_score(plant_type: str, conditions: SensorData) -> tuple[int, Dict[str, int], List[str], List[str]]:
    """Calculate overall plant health score and identify issues"""
    if plant_type not in PLANT_DATABASE:
        raise ValueError(f"Unknown plant type: {plant_type}")
    
    plant_data = PLANT_DATABASE[plant_type]
    optimal_conditions = plant_data["optimal_conditions"]
    
    # Calculate scores for each parameter
    parameter_scores = {}
    critical_issues = []
    recommendations = []
    
    # Temperature
    temp_score = calculate_parameter_score(conditions.temperature, optimal_conditions["temperature"])
    parameter_scores["temperature"] = temp_score
    if temp_score < 60:
        critical_issues.append("Temperature outside optimal range")
        if conditions.temperature < optimal_conditions["temperature"]["min"]:
            recommendations.append("Move plant to warmer location or provide heating")
        else:
            recommendations.append("Provide shade or cooling")
    
    # Humidity
    humidity_score = calculate_parameter_score(conditions.humidity, optimal_conditions["humidity"])
    parameter_scores["humidity"] = humidity_score
    if humidity_score < 60:
        critical_issues.append("Humidity outside optimal range")
        if conditions.humidity < optimal_conditions["humidity"]["min"]:
            recommendations.append("Increase humidity with misting or humidifier")
        else:
            recommendations.append("Improve air circulation to reduce humidity")
    
    # Soil Moisture
    moisture_score = calculate_parameter_score(conditions.soil_moisture, optimal_conditions["soil_moisture"])
    parameter_scores["soil_moisture"] = moisture_score
    if moisture_score < 60:
        critical_issues.append("Soil moisture outside optimal range")
        if conditions.soil_moisture < optimal_conditions["soil_moisture"]["min"]:
            recommendations.append("Increase watering frequency")
        else:
            recommendations.append("Reduce watering and improve drainage")
    
    # Light Intensity
    light_score = calculate_parameter_score(conditions.light_intensity, optimal_conditions["light_intensity"])
    parameter_scores["light_intensity"] = light_score
    if light_score < 60:
        critical_issues.append("Light intensity outside optimal range")
        if conditions.light_intensity < optimal_conditions["light_intensity"]["min"]:
            recommendations.append("Move to brighter location or add grow lights")
        else:
            recommendations.append("Provide shade to prevent light burn")
    
    # Soil pH
    ph_score = calculate_parameter_score(conditions.soil_ph, optimal_conditions["soil_ph"])
    parameter_scores["soil_ph"] = ph_score
    if ph_score < 60:
        critical_issues.append("Soil pH outside optimal range")
        if conditions.soil_ph < optimal_conditions["soil_ph"]["min"]:
            recommendations.append("Add lime to increase soil pH")
        else:
            recommendations.append("Add sulfur or peat moss to lower soil pH")
    
    # Calculate overall health score
    overall_score = int(sum(parameter_scores.values()) / len(parameter_scores))
    
    return overall_score, parameter_scores, critical_issues, recommendations

# API Endpoints
@router.get("/{plant_name}/optimal-ranges", response_model=OptimalRangesResponse)
async def get_optimal_ranges(plant_name: str):
    """Get optimal parameter ranges for a specific plant"""
    if plant_name not in PLANT_DATABASE:
        raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
    
    plant_data = PLANT_DATABASE[plant_name]
    
    return OptimalRangesResponse(
        plant_name=plant_data["name"],
        optimal_conditions=plant_data["optimal_conditions"],
        growth_stages=plant_data["growth_stages"],
        common_issues=plant_data["common_issues"]
    )

@router.post("/{plant_name}/analyze", response_model=HealthScoreResponse)
async def analyze_plant_conditions(plant_name: str, conditions: SensorData):
    """Analyze current plant conditions and calculate health score"""
    if plant_name not in PLANT_DATABASE:
        raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
    
    try:
        health_score, parameter_scores, critical_issues, recommendations = calculate_health_score(plant_name, conditions)
        
        return HealthScoreResponse(
            plant_type=plant_name,
            health_score=health_score,
            parameter_scores=parameter_scores,
            critical_issues=critical_issues,
            recommendations=recommendations
        )
    except Exception as e:
        logger.error(f"Error analyzing plant conditions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze plant conditions")

@router.post("/{plant_name}/ai-advice", response_model=PlantAIAnalysisResponse)
async def get_ai_advice(plant_name: str, request: PlantAIAnalysisRequest):
    """Get AI-powered gardening advice for a specific plant"""
    if plant_name not in PLANT_DATABASE:
        raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
    
    try:
        # Calculate health score and issues
        health_score, parameter_scores, critical_issues, recommendations = calculate_health_score(
            plant_name, request.current_conditions
        )
        
        # Get plant data for context
        plant_data = PLANT_DATABASE[plant_name]
        
        # Create comprehensive prompt for AI
        growing_season_info = ""
        if 'growing_season' in plant_data:
            season = plant_data['growing_season']
            growing_season_info = f"""
GROWING SEASON INFORMATION:
- Best growing months: {', '.join(season['best_months'])}
- Planting time: {season['planting_time']}
- Harvest time: {season['harvest_time']}
- Temperature range: {season['temperature_range']}
- Seasonal notes: {season['seasonal_notes']}
"""

        prompt = f"""
You are an expert gardening advisor specializing in {plant_data['name']} care. 

PLANT INFORMATION:
- Plant: {plant_data['name']}
- Growth Stage: {request.current_conditions.growth_stage}
- Location: {request.current_conditions.location}
{growing_season_info}
CURRENT CONDITIONS:
- Temperature: {request.current_conditions.temperature}°C
- Humidity: {request.current_conditions.humidity}%
- Soil Moisture: {request.current_conditions.soil_moisture}%
- Light Intensity: {request.current_conditions.light_intensity} lux
- Soil pH: {request.current_conditions.soil_ph}

HEALTH ANALYSIS:
- Overall Health Score: {health_score}/100
- Critical Issues: {', '.join(critical_issues) if critical_issues else 'None'}
- Recommendations: {', '.join(recommendations) if recommendations else 'None'}

USER QUESTION: {request.user_question}

CHAT HISTORY:
{chr(10).join([f"{msg.role}: {msg.content}" for msg in request.chat_history[-3:]])}

IMPORTANT: Answer the user's specific question directly and concisely. Focus on the exact question asked.

For growing season questions, provide specific information about:
- When to plant {plant_data['name']}
- Best months for growing
- Seasonal care requirements
- Temperature and weather considerations

Be conversational, helpful, and specific to {plant_data['name']} care. Keep your response focused and relevant to the question asked.
"""
        
        # Get AI advice
        ai_response = await deepseek_client.get_advice(prompt)
        
        # If AI is not available, provide intelligent fallback with growing season info
        if not ai_response or "unable to provide AI advice" in ai_response:
            ai_response = _create_intelligent_fallback(plant_data, request.user_question, health_score, critical_issues, recommendations)
        
        return PlantAIAnalysisResponse(
            success=True,
            advice=ai_response,
            health_score=health_score,
            critical_issues=critical_issues,
            recommendations=recommendations,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
    except Exception as e:
        logger.error(f"Error getting AI advice: {str(e)}")
        # Use intelligent fallback with growing season info
        plant_data = PLANT_DATABASE[plant_name]
        fallback_advice = _create_intelligent_fallback(plant_data, request.user_question, health_score, critical_issues, recommendations)
        return PlantAIAnalysisResponse(
            success=True,
            advice=fallback_advice,
            health_score=health_score if 'health_score' in locals() else 50,
            critical_issues=critical_issues if 'critical_issues' in locals() else [],
            recommendations=recommendations if 'recommendations' in locals() else [],
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

def _create_intelligent_fallback(plant_data: Dict[str, Any], user_question: str, 
                                health_score: int, critical_issues: List[str], 
                                recommendations: List[str]) -> str:
    """
    Create intelligent fallback response with growing season information
    """
    plant_name = plant_data['name']
    
    # Check if question is about growing season
    growing_season_keywords = ['growing season', 'when to plant', 'best months', 'planting time', 'harvest time', 'season', 'months', 'plant']
    is_growing_season_question = any(keyword in user_question.lower() for keyword in growing_season_keywords)
    
    if is_growing_season_question and 'growing_season' in plant_data:
        season = plant_data['growing_season']
        response = f"""🌱 **Growing Season for {plant_name}**

**Best Growing Months:** {', '.join(season['best_months'])}

**Planting Time:** {season['planting_time']}

**Harvest Time:** {season['harvest_time']}

**Temperature Range:** {season['temperature_range']}

**Seasonal Notes:** {season['seasonal_notes']}

**Current Health Score:** {health_score}/100

"""
        if critical_issues:
            response += f"\n**⚠️ Critical Issues:** {', '.join(critical_issues)}"
        
        if recommendations:
            response += f"\n**💡 Recommendations:** {', '.join(recommendations)}"
            
        return response
    
    # General fallback for other questions
    return f"""I'm currently unable to access AI-powered advice, but here's some basic guidance for your {plant_name}:

**Current Health Score:** {health_score}/100

**Current Issues:** {', '.join(critical_issues) if critical_issues else 'None detected'}

**Recommendations:** {', '.join(recommendations) if recommendations else 'Continue current care routine'}

For more specific advice, please ensure your DeepSeek API key is properly configured."""

@router.post("/{plant_name}/health-score", response_model=HealthScoreResponse)
async def get_health_score(plant_name: str, conditions: SensorData):
    """Get current health score for a plant"""
    if plant_name not in PLANT_DATABASE:
        raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
    
    try:
        health_score, parameter_scores, critical_issues, recommendations = calculate_health_score(plant_name, conditions)
        
        return HealthScoreResponse(
            plant_type=plant_name,
            health_score=health_score,
            parameter_scores=parameter_scores,
            critical_issues=critical_issues,
            recommendations=recommendations
        )
    except Exception as e:
        logger.error(f"Error calculating health score: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate health score")
