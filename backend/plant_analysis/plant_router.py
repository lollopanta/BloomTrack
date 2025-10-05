"""
Plant Analysis Router for BloomTracker Plant Sensor Analysis System.

This module provides FastAPI endpoints for plant sensor data analysis,
AI-powered gardening advice, and real-time sensor data simulation.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .plant_database import plant_db
from .plant_advisor import plant_advisor, PlantAnalysis, HealthStatus
from .deepseek_client import deepseek_client

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/plants", tags=["Plant Analysis"])

# Pydantic models for request/response
class PlantSensorData(BaseModel):
    """Plant sensor data model."""
    plant_type: str = Field(..., description="Type of plant (chili_pepper, grapevine, olive_tree)")
    temperature: float = Field(..., ge=0, le=50, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    light_intensity: float = Field(..., ge=0, le=2000, description="Light intensity in lux")
    soil_ph: float = Field(..., ge=4.0, le=9.0, description="Soil pH level")
    growth_stage: str = Field(..., description="Growth stage (germination, vegetative, flowering, fruiting, etc.)")
    location: str = Field(default="Indoor", description="Plant location")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Timestamp of sensor reading")

class SensorReadingResponse(BaseModel):
    """Individual sensor reading response."""
    parameter: str
    current_value: float
    optimal_min: float
    optimal_max: float
    optimal_target: float
    health_score: float
    status: str
    recommendation: str

class PlantAnalysisResponse(BaseModel):
    """Complete plant analysis response."""
    plant_name: str
    growth_stage: str
    overall_health_score: float
    overall_status: str
    sensor_readings: List[SensorReadingResponse]
    critical_issues: List[str]
    recommendations: List[str]
    ai_advice: Optional[str] = None
    analysis_timestamp: datetime

class PlantInfo(BaseModel):
    """Basic plant information."""
    name: str
    scientific_name: str
    category: str
    key: str

class SimulatedDataRequest(BaseModel):
    """Request for simulated sensor data."""
    plant_name: str = Field(..., description="Name of the plant")
    growth_stage: str = Field(..., description="Growth stage")
    location: str = Field(default="Indoor", description="Plant location")

class SimulatedDataInput(BaseModel):
    """Input for simulated data from frontend sliders."""
    plant_type: str = Field(..., description="Type of plant (chili_pepper, grapevine, olive_tree)")
    temperature: float = Field(..., ge=0, le=50, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    light_intensity: float = Field(..., ge=0, le=20000, description="Light intensity in lux")
    soil_ph: float = Field(..., ge=4.0, le=9.0, description="Soil pH level")

class SimulatedDataResponse(BaseModel):
    """Response for simulated data endpoint."""
    plant_type: str
    temperature: float
    humidity: float
    soil_moisture: float
    light_intensity: float
    soil_ph: float
    timestamp: datetime
    status: str

class AIAdviceRequest(BaseModel):
    """Request for AI-powered plant advice."""
    plant_type: str = Field(..., description="Type of plant (chili_pepper, grapevine, olive_tree)")
    current_conditions: Dict[str, Any] = Field(..., description="Current sensor readings and conditions")
    user_question: str = Field(..., description="User's specific question about plant care")

class AIAdviceResponse(BaseModel):
    """Response for AI advice endpoint."""
    success: bool
    advice: str
    plant_type: str
    timestamp: datetime
    ai_available: bool = True

# API Endpoints

@router.get("/", response_model=List[PlantInfo])
async def get_plants():
    """Get list of available plants with basic information."""
    try:
        plants = plant_db.get_plant_list()
        logger.info(f"Retrieved {len(plants)} plants from database")
        return plants
    except Exception as e:
        logger.error(f"Error retrieving plants: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving plant list")

@router.get("/{plant_name}/parameters", response_model=Dict[str, Any])
async def get_plant_parameters(plant_name: str):
    """Get detailed parameters for a specific plant."""
    try:
        parameters = plant_db.get_plant_parameters(plant_name)
        if not parameters:
            raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
        
        logger.info(f"Retrieved parameters for plant: {plant_name}")
        return parameters
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving plant parameters for {plant_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving plant parameters")

@router.post("/analyze", response_model=PlantAnalysisResponse)
async def analyze_sensor_data(sensor_data: PlantSensorData):
    """Analyze sensor data and return growth recommendations."""
    try:
        # Convert Pydantic model to dict
        sensor_dict = sensor_data.dict()
        
        # Perform analysis
        analysis = plant_advisor.analyze_sensor_data(sensor_dict, sensor_data.plant_type)
        
        # Convert sensor readings to response format
        sensor_readings = [
            SensorReadingResponse(
                parameter=reading.parameter,
                current_value=reading.current_value,
                optimal_min=reading.optimal_min,
                optimal_max=reading.optimal_max,
                optimal_target=reading.optimal_target,
                health_score=reading.health_score,
                status=reading.status.value,
                recommendation=reading.recommendation
            )
            for reading in analysis.sensor_readings
        ]
        
        response = PlantAnalysisResponse(
            plant_name=analysis.plant_name,
            growth_stage=analysis.growth_stage,
            overall_health_score=analysis.overall_health_score,
            overall_status=analysis.overall_status.value,
            sensor_readings=sensor_readings,
            critical_issues=analysis.critical_issues,
            recommendations=analysis.recommendations,
            ai_advice=analysis.ai_advice,
            analysis_timestamp=datetime.now()
        )
        
        logger.info(f"Analysis completed for {sensor_data.plant_type} - Health Score: {analysis.overall_health_score:.2f}")
        return response
        
    except ValueError as e:
        logger.warning(f"Invalid plant or growth stage: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing sensor data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing sensor data")

@router.get("/simulated-data", response_model=PlantSensorData)
async def get_simulated_data(
    plant_name: str,
    growth_stage: str,
    location: str = "Indoor"
):
    """Generate realistic simulated sensor data for testing."""
    try:
        simulated_data = plant_advisor.generate_simulated_data(plant_name, growth_stage, location)
        
        # Convert to PlantSensorData model
        sensor_data = PlantSensorData(**simulated_data)
        
        logger.info(f"Generated simulated data for {plant_name} in {growth_stage} stage")
        return sensor_data
        
    except ValueError as e:
        logger.warning(f"Invalid parameters for simulated data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating simulated data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating simulated data")

@router.post("/ai-advice", response_model=Dict[str, str])
async def get_ai_advice(sensor_data: PlantSensorData):
    """Get personalized AI gardening advice using DeepSeek API."""
    try:
        # Get plant data
        plant_data = plant_db.get_plant_parameters(sensor_data.plant_type)
        if not plant_data:
            raise HTTPException(status_code=404, detail=f"Plant '{sensor_data.plant_type}' not found")
        
        # Convert sensor data to dict
        sensor_dict = sensor_data.dict()
        
        # Get AI advice
        ai_advice = plant_advisor.deepseek_client.get_gardening_advice(plant_data, sensor_dict)
        
        logger.info(f"Generated AI advice for {sensor_data.plant_type}")
        return {"advice": ai_advice}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting AI advice: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting AI advice")

@router.get("/health-status/{plant_name}/{growth_stage}")
async def get_health_status_info(plant_name: str, growth_stage: str):
    """Get health status information and color codes for a plant and growth stage."""
    try:
        # Get plant parameters
        plant_data = plant_db.get_plant_parameters(plant_name)
        if not plant_data:
            raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
        
        # Get optimal conditions
        optimal_conditions = plant_db.get_optimal_conditions(plant_name, growth_stage)
        if not optimal_conditions:
            raise HTTPException(status_code=404, detail=f"Growth stage '{growth_stage}' not found for {plant_name}")
        
        # Get health indicators
        health_indicators = plant_db.get_plant_health_indicators(plant_name, growth_stage)
        
        # Add color codes for health status
        status_colors = {
            "excellent": "#10B981",
            "good": "#3B82F6",
            "warning": "#F59E0B",
            "critical": "#EF4444"
        }
        
        response = {
            "plant_name": plant_name,
            "growth_stage": growth_stage,
            "optimal_conditions": optimal_conditions,
            "health_indicators": health_indicators,
            "status_colors": status_colors
        }
        
        logger.info(f"Retrieved health status info for {plant_name} - {growth_stage}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting health status info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting health status information")

@router.get("/growth-stages/{plant_name}")
async def get_growth_stages(plant_name: str):
    """Get available growth stages for a specific plant."""
    try:
        plant_data = plant_db.get_plant_parameters(plant_name)
        if not plant_data:
            raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
        
        growth_stages = list(plant_data["growth_stages"].keys())
        
        logger.info(f"Retrieved {len(growth_stages)} growth stages for {plant_name}")
        return {"plant_name": plant_name, "growth_stages": growth_stages}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting growth stages: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting growth stages")

@router.get("/care-requirements/{plant_name}")
async def get_care_requirements(plant_name: str):
    """Get care requirements and common issues for a plant."""
    try:
        plant_data = plant_db.get_plant_parameters(plant_name)
        if not plant_data:
            raise HTTPException(status_code=404, detail=f"Plant '{plant_name}' not found")
        
        care_info = {
            "care_requirements": plant_data["care_requirements"],
            "common_issues": plant_data["common_issues"],
            "harvesting": plant_data["harvesting"]
        }
        
        logger.info(f"Retrieved care requirements for {plant_name}")
        return care_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting care requirements: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting care requirements")

@router.post("/simulated-data", response_model=SimulatedDataResponse)
async def receive_simulated_data(data: SimulatedDataInput):
    """Receive simulated sensor data from frontend sliders."""
    try:
        # Validate plant type
        valid_plant_types = ["chili_pepper", "grapevine", "olive_tree"]
        if data.plant_type not in valid_plant_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid plant type. Must be one of: {', '.join(valid_plant_types)}"
            )
        
        # Create response with timestamp and status
        response = SimulatedDataResponse(
            plant_type=data.plant_type,
            temperature=data.temperature,
            humidity=data.humidity,
            soil_moisture=data.soil_moisture,
            light_intensity=data.light_intensity,
            soil_ph=data.soil_ph,
            timestamp=datetime.now(),
            status="received"
        )
        
        logger.info(f"Received simulated data for {data.plant_type}: "
                   f"T={data.temperature}°C, H={data.humidity}%, "
                   f"SM={data.soil_moisture}%, LI={data.light_intensity}lux, pH={data.soil_ph}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing simulated data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing simulated data")

@router.post("/ai-advice", response_model=AIAdviceResponse)
async def get_ai_advice(request: AIAdviceRequest):
    """Get AI-powered gardening advice using DeepSeek API."""
    try:
        # Validate plant type
        valid_plant_types = ["chili_pepper", "grapevine", "olive_tree"]
        if request.plant_type not in valid_plant_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid plant type. Must be one of: {', '.join(valid_plant_types)}"
            )
        
        # Get plant data from database
        plant_data = plant_db.get_plant_parameters(request.plant_type)
        if not plant_data:
            raise HTTPException(status_code=404, detail=f"Plant '{request.plant_type}' not found")
        
        # Validate current conditions
        required_conditions = ['temperature', 'humidity', 'soil_moisture', 'light_intensity', 'soil_ph']
        for condition in required_conditions:
            if condition not in request.current_conditions:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing required condition: {condition}"
                )
        
        # Check if DeepSeek is available
        ai_available = deepseek_client._is_available()
        
        # Get AI advice
        logger.info(f"Generating AI advice for {request.plant_type} plant")
        advice = await deepseek_client.get_gardening_advice(
            plant_data=plant_data,
            current_conditions=request.current_conditions,
            user_question=request.user_question
        )
        
        response = AIAdviceResponse(
            success=True,
            advice=advice,
            plant_type=request.plant_type,
            timestamp=datetime.now(),
            ai_available=ai_available
        )
        
        logger.info(f"AI advice generated successfully for {request.plant_type}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating AI advice: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating AI advice")
