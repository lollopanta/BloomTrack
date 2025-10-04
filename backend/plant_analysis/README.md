# Plant Sensor Analysis & Advisor System

This module provides comprehensive plant sensor data analysis, AI-powered gardening advice, and real-time sensor data simulation for the BloomTracker application.

## 🌱 Features

- **Plant Database**: Comprehensive knowledge base for Chili Pepper, Grapevine, and Olive Tree
- **Sensor Analysis**: Real-time analysis of temperature, humidity, soil moisture, light intensity, and soil pH
- **AI Integration**: DeepSeek AI-powered personalized gardening advice
- **Health Scoring**: Intelligent health assessment with color-coded indicators
- **Real-time Simulation**: Dynamic sensor data generation for testing and demonstration
- **Growth Stage Support**: Plant-specific optimal conditions for different growth stages

## 📁 Module Structure

```
plant_analysis/
├── __init__.py              # Module initialization
├── plant_database.py        # Plant knowledge base and data models
├── plant_advisor.py         # Analysis logic and AI integration
├── plant_router.py          # FastAPI router with all endpoints
└── README.md               # This documentation
```

## 🚀 API Endpoints

### Plant Information

- `GET /plants/` - List all available plants
- `GET /plants/{plant_name}/parameters` - Get detailed plant parameters
- `GET /plants/growth-stages/{plant_name}` - Get available growth stages
- `GET /plants/care-requirements/{plant_name}` - Get care requirements

### Sensor Analysis

- `POST /plants/analyze` - Analyze sensor data and get recommendations
- `GET /plants/simulated-data` - Generate realistic simulated sensor data
- `POST /plants/ai-advice` - Get AI-powered gardening advice

### Health Status

- `GET /plants/health-status/{plant_name}/{growth_stage}` - Get health status information

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# DeepSeek AI API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### API Key Setup

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account and generate an API key
3. Add the key to your `.env` file
4. Restart the backend server

## 📊 Plant Database

### Supported Plants

1. **Chili Pepper (Capsicum annuum)**

   - Growth stages: germination, vegetative, flowering, fruiting
   - Optimal temperature: 18-30°C
   - Light requirements: 200-1000 lux
   - Soil pH: 6.0-7.0

2. **Grapevine (Vitis vinifera)**

   - Growth stages: dormancy, bud_break, vegetative, flowering, fruit_development, ripening
   - Optimal temperature: -5-30°C (seasonal)
   - Light requirements: 0-1200 lux (seasonal)
   - Soil pH: 6.0-7.5

3. **Olive Tree (Olea europaea)**
   - Growth stages: dormancy, bud_break, vegetative, flowering, fruit_development, ripening
   - Optimal temperature: -5-30°C (seasonal)
   - Light requirements: 200-1200 lux
   - Soil pH: 6.5-8.5

### Sensor Parameters

Each plant has optimal ranges for:

- **Temperature** (°C): Air temperature
- **Humidity** (%): Relative humidity
- **Soil Moisture** (%): Soil water content
- **Light Intensity** (lux): Light exposure
- **Soil pH**: Soil acidity/alkalinity

## 🤖 AI Integration

### DeepSeek AI Features

- **Personalized Advice**: Plant-specific recommendations based on sensor data
- **Growth Stage Awareness**: Advice tailored to current growth stage
- **Problem Diagnosis**: Identification of common plant issues
- **Actionable Recommendations**: Specific steps to improve plant health

### Response Caching

- **Cache Key**: Plant name + sensor data hash
- **Cache Duration**: Session-based (until server restart)
- **Fallback**: Graceful degradation when AI is unavailable

## 📈 Health Analysis

### Health Scoring System

- **Excellent** (80-100%): All parameters within optimal range
- **Good** (60-79%): Most parameters acceptable
- **Warning** (40-59%): Some parameters need attention
- **Critical** (0-39%): Immediate action required

### Color Coding

- 🟢 **Green**: Excellent health
- 🔵 **Blue**: Good health
- 🟡 **Yellow**: Warning status
- 🔴 **Red**: Critical issues

## 🔄 Real-time Simulation

### Dynamic Data Generation

The simulator generates realistic sensor data based on:

- **Time of Day**: Light intensity varies with time
- **Seasonal Patterns**: Temperature and humidity changes
- **Growth Stage**: Different optimal conditions per stage
- **Random Variation**: Natural fluctuations in readings

### Simulation Parameters

```python
# Example simulated data
{
    "plant_type": "chili_pepper",
    "temperature": 23.5,
    "humidity": 65.2,
    "soil_moisture": 58.7,
    "light_intensity": 650,
    "soil_ph": 6.4,
    "growth_stage": "vegetative",
    "location": "Indoor",
    "timestamp": "2025-01-05T10:30:00Z"
}
```

## 🎯 Usage Examples

### Basic Analysis

```python
# Analyze sensor data
sensor_data = {
    "plant_type": "chili_pepper",
    "temperature": 25.0,
    "humidity": 70.0,
    "soil_moisture": 60.0,
    "light_intensity": 600.0,
    "soil_ph": 6.5,
    "growth_stage": "vegetative",
    "location": "Indoor"
}

# POST /plants/analyze
response = requests.post("http://localhost:8000/plants/analyze", json=sensor_data)
analysis = response.json()
```

### Generate Simulated Data

```python
# GET /plants/simulated-data
response = requests.get(
    "http://localhost:8000/plants/simulated-data",
    params={
        "plant_name": "chili_pepper",
        "growth_stage": "vegetative",
        "location": "Indoor"
    }
)
simulated_data = response.json()
```

### Get AI Advice

```python
# POST /plants/ai-advice
response = requests.post("http://localhost:8000/plants/ai-advice", json=sensor_data)
advice = response.json()["advice"]
```

## 🛠️ Development

### Adding New Plants

1. Add plant data to `plant_database.py`
2. Include all growth stages and optimal conditions
3. Add care requirements and common issues
4. Test with simulated data generation

### Extending AI Integration

1. Modify `DeepSeekClient` in `plant_advisor.py`
2. Update prompt formatting for better AI responses
3. Add response caching for performance
4. Implement fallback mechanisms

### Custom Health Scoring

1. Modify `_analyze_parameter` method in `PlantAdvisor`
2. Adjust scoring algorithms for different parameters
3. Add custom health indicators
4. Implement plant-specific scoring rules

## 🔍 Troubleshooting

### Common Issues

1. **AI Advice Unavailable**

   - Check `DEEPSEEK_API_KEY` environment variable
   - Verify API key is valid and has credits
   - Check network connectivity

2. **Plant Not Found**

   - Verify plant name spelling
   - Check available plants with `GET /plants/`
   - Ensure plant is in database

3. **Invalid Growth Stage**
   - Check available growth stages for plant
   - Use `GET /plants/growth-stages/{plant_name}`
   - Verify stage name spelling

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger("plant_analysis").setLevel(logging.DEBUG)
```

## 📚 Dependencies

- `fastapi`: Web framework
- `pydantic`: Data validation
- `requests`: HTTP client for AI API
- `datetime`: Timestamp handling
- `logging`: Application logging

## 🤝 Contributing

1. Follow existing code patterns
2. Add comprehensive docstrings
3. Include error handling
4. Update documentation
5. Test with multiple plant types

## 📄 License

This module is part of the BloomTracker project and follows the same licensing terms.
