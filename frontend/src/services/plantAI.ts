import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Types
export interface SensorData {
  temperature: number;
  humidity: number;
  soilMoisture: number;
  lightIntensity: number;
  soilPh: number;
  growthStage: string;
  location: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface PlantAIAnalysisRequest {
  plant_type: string;
  current_conditions: SensorData;
  user_question: string;
  chat_history: ChatMessage[];
}

export interface PlantAIAnalysisResponse {
  success: boolean;
  advice: string;
  health_score: number;
  critical_issues: string[];
  recommendations: string[];
  timestamp: string;
}

export interface OptimalRangesResponse {
  plant_name: string;
  optimal_conditions: {
    temperature: { min: number; max: number; optimal: number };
    humidity: { min: number; max: number; optimal: number };
    soil_moisture: { min: number; max: number; optimal: number };
    light_intensity: { min: number; max: number; optimal: number };
    soil_ph: { min: number; max: number; optimal: number };
  };
  growth_stages: string[];
  common_issues: string[];
}

export interface HealthScoreResponse {
  plant_type: string;
  health_score: number;
  parameter_scores: {
    temperature: number;
    humidity: number;
    soil_moisture: number;
    light_intensity: number;
    soil_ph: number;
  };
  critical_issues: string[];
  recommendations: string[];
}

// API Service Class
class PlantAIService {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  // Get optimal parameter ranges for a plant
  async getOptimalRanges(plantName: string): Promise<OptimalRangesResponse> {
    try {
      const response = await axios.get(`${this.baseURL}/plants/${plantName}/optimal-ranges`);
      return response.data;
    } catch (error) {
      console.error('Error fetching optimal ranges:', error);
      throw new Error('Failed to fetch optimal ranges');
    }
  }

  // Analyze current plant conditions
  async analyzePlantConditions(plantName: string, conditions: SensorData): Promise<HealthScoreResponse> {
    try {
      const response = await axios.post(`${this.baseURL}/plants/${plantName}/analyze`, conditions);
      return response.data;
    } catch (error) {
      console.error('Error analyzing plant conditions:', error);
      throw new Error('Failed to analyze plant conditions');
    }
  }

  // Get AI-powered gardening advice
  async getAIAdvice(plantName: string, request: PlantAIAnalysisRequest): Promise<PlantAIAnalysisResponse> {
    try {
      const response = await axios.post(`${this.baseURL}/plants/${plantName}/ai-advice`, request);
      return response.data;
    } catch (error) {
      console.error('Error getting AI advice:', error);
      throw new Error('Failed to get AI advice');
    }
  }

  // Get health score for a plant
  async getHealthScore(plantName: string, conditions: SensorData): Promise<HealthScoreResponse> {
    try {
      const response = await axios.get(`${this.baseURL}/plants/${plantName}/health-score`, {
        params: conditions
      });
      return response.data;
    } catch (error) {
      console.error('Error getting health score:', error);
      throw new Error('Failed to get health score');
    }
  }

  // Simulate sensor data (for testing)
  generateSimulatedData(plantType: string): SensorData {
    const baseData = {
      chili_pepper: {
        temperature: 25,
        humidity: 60,
        soilMoisture: 65,
        lightIntensity: 9000,
        soilPh: 6.5
      },
      grapevine: {
        temperature: 25,
        humidity: 45,
        soilMoisture: 55,
        lightIntensity: 12000,
        soilPh: 6.8
      },
      olive_tree: {
        temperature: 25,
        humidity: 35,
        soilMoisture: 45,
        lightIntensity: 15000,
        soilPh: 7.2
      }
    };

    const base = baseData[plantType as keyof typeof baseData] || baseData.chili_pepper;
    
    return {
      ...base,
      growthStage: 'vegetative',
      location: 'indoor'
    };
  }

  // Calculate health score locally (fallback)
  calculateHealthScore(conditions: SensorData, optimal: any): {
    overall: number;
    parameters: { [key: string]: number };
    criticalIssues: string[];
    recommendations: string[];
  } {
    const calculateParameterScore = (value: number, range: { min: number; max: number; optimal: number }) => {
      if (value >= range.min && value <= range.max) {
        const distanceFromOptimal = Math.abs(value - range.optimal);
        const rangeSize = range.max - range.min;
        return Math.max(0, 100 - (distanceFromOptimal / (rangeSize / 2)) * 50);
      }
      return Math.max(0, 50 - Math.abs(value - (value < range.min ? range.min : range.max)) * 10);
    };

    const tempScore = calculateParameterScore(conditions.temperature, optimal.temperature);
    const humidityScore = calculateParameterScore(conditions.humidity, optimal.humidity);
    const moistureScore = calculateParameterScore(conditions.soilMoisture, optimal.soil_moisture);
    const lightScore = calculateParameterScore(conditions.lightIntensity, optimal.light_intensity);
    const phScore = calculateParameterScore(conditions.soilPh, optimal.soil_ph);

    const overall = Math.round((tempScore + humidityScore + moistureScore + lightScore + phScore) / 5);
    
    const criticalIssues = [];
    const recommendations = [];

    if (tempScore < 60) {
      criticalIssues.push('Temperature outside optimal range');
      if (conditions.temperature < optimal.temperature.min) {
        recommendations.push('Move plant to warmer location');
      } else {
        recommendations.push('Provide shade or cooling');
      }
    }

    if (humidityScore < 60) {
      criticalIssues.push('Humidity outside optimal range');
      if (conditions.humidity < optimal.humidity.min) {
        recommendations.push('Increase humidity with misting');
      } else {
        recommendations.push('Improve air circulation');
      }
    }

    if (moistureScore < 60) {
      criticalIssues.push('Soil moisture outside optimal range');
      if (conditions.soilMoisture < optimal.soil_moisture.min) {
        recommendations.push('Increase watering frequency');
      } else {
        recommendations.push('Reduce watering and improve drainage');
      }
    }

    if (lightScore < 60) {
      criticalIssues.push('Light intensity outside optimal range');
      if (conditions.lightIntensity < optimal.light_intensity.min) {
        recommendations.push('Move to brighter location');
      } else {
        recommendations.push('Provide shade to prevent light burn');
      }
    }

    if (phScore < 60) {
      criticalIssues.push('Soil pH outside optimal range');
      if (conditions.soilPh < optimal.soil_ph.min) {
        recommendations.push('Add lime to increase soil pH');
      } else {
        recommendations.push('Add sulfur to lower soil pH');
      }
    }

    return {
      overall,
      parameters: {
        temperature: tempScore,
        humidity: humidityScore,
        soilMoisture: moistureScore,
        lightIntensity: lightScore,
        soilPh: phScore
      },
      criticalIssues,
      recommendations
    };
  }
}

// Export singleton instance
export const plantAIService = new PlantAIService();

// Export types
export type { SensorData, ChatMessage, PlantAIAnalysisRequest, PlantAIAnalysisResponse, OptimalRangesResponse, HealthScoreResponse };
