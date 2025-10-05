# DeepSeek AI Integration for BloomTracker

## Overview

This document describes the DeepSeek AI integration added to the BloomTracker backend, providing AI-powered gardening advice for plant care.

## Features

- **AI-Powered Plant Advice**: Get personalized gardening recommendations using DeepSeek AI
- **Intelligent Prompt Engineering**: Combines plant database knowledge with current sensor data
- **Graceful Fallback**: Provides basic advice when AI is unavailable
- **Rate Limiting & Error Handling**: Robust API communication with retry logic
- **Multi-Plant Support**: Works with Chili Pepper, Grapevine, and Olive Tree

## API Endpoint

### POST `/plants/ai-advice`

Get AI-powered gardening advice for your plants.

#### Request Body

```json
{
  "plant_type": "chili_pepper",
  "current_conditions": {
    "temperature": 25.5,
    "humidity": 65.0,
    "soil_moisture": 70.0,
    "light_intensity": 800.0,
    "soil_ph": 6.5,
    "growth_stage": "vegetative",
    "location": "indoor"
  },
  "user_question": "Why are my leaves turning yellow?"
}
```

#### Response Body

```json
{
  "success": true,
  "advice": "Based on your Chili Pepper's current conditions...",
  "plant_type": "chili_pepper",
  "timestamp": "2024-01-15T10:30:00Z",
  "ai_available": true
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `plant_type` | string | Yes | Plant type: `chili_pepper`, `grapevine`, `olive_tree` |
| `current_conditions` | object | Yes | Current sensor readings and conditions |
| `current_conditions.temperature` | number | Yes | Temperature in Celsius (0-50) |
| `current_conditions.humidity` | number | Yes | Humidity percentage (0-100) |
| `current_conditions.soil_moisture` | number | Yes | Soil moisture percentage (0-100) |
| `current_conditions.light_intensity` | number | Yes | Light intensity in lux (0-20000) |
| `current_conditions.soil_ph` | number | Yes | Soil pH level (4.0-9.0) |
| `current_conditions.growth_stage` | string | Yes | Growth stage (germination, vegetative, flowering, fruiting) |
| `current_conditions.location` | string | No | Plant location (default: "indoor") |
| `user_question` | string | Yes | User's specific question about plant care |

## Setup

### 1. Environment Configuration

The project uses `.env` files for environment variable management:

#### Option A: Automatic Setup (Recommended)
```bash
python setup_env.py
```

#### Option B: Manual Setup
1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` file and set your API key:
   ```bash
   # Edit .env file
   DEEPSEEK_API_KEY=your_actual_deepseek_api_key_here
   ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

```bash
python main.py
```

## Usage Examples

### Example 1: Basic Plant Care Question

```bash
curl -X POST "http://localhost:8000/plants/ai-advice" \
  -H "Content-Type: application/json" \
  -d '{
    "plant_type": "chili_pepper",
    "current_conditions": {
      "temperature": 25.5,
      "humidity": 65.0,
      "soil_moisture": 70.0,
      "light_intensity": 800.0,
      "soil_ph": 6.5,
      "growth_stage": "vegetative",
      "location": "indoor"
    },
    "user_question": "Why are my leaves turning yellow?"
  }'
```

### Example 2: Grapevine Care

```bash
curl -X POST "http://localhost:8000/plants/ai-advice" \
  -H "Content-Type: application/json" \
  -d '{
    "plant_type": "grapevine",
    "current_conditions": {
      "temperature": 22.0,
      "humidity": 60.0,
      "soil_moisture": 65.0,
      "light_intensity": 1200.0,
      "soil_ph": 6.8,
      "growth_stage": "flowering",
      "location": "outdoor"
    },
    "user_question": "How often should I water my grapevine during flowering?"
  }'
```

### Example 3: Olive Tree Maintenance

```bash
curl -X POST "http://localhost:8000/plants/ai-advice" \
  -H "Content-Type: application/json" \
  -d '{
    "plant_type": "olive_tree",
    "current_conditions": {
      "temperature": 18.0,
      "humidity": 55.0,
      "soil_moisture": 40.0,
      "light_intensity": 1500.0,
      "soil_ph": 7.2,
      "growth_stage": "fruiting",
      "location": "outdoor"
    },
    "user_question": "Is my olive tree getting enough water?"
  }'
```

## AI Prompt Engineering

The system creates intelligent prompts that combine:

1. **Plant Database Knowledge**: Optimal conditions for each growth stage
2. **Current Sensor Data**: Real-time readings from user's sensors
3. **User Questions**: Specific concerns or questions
4. **Contextual Information**: Growth stage, location, and plant type

### Example Generated Prompt

```
You are an expert horticulturist and plant care specialist. Provide detailed, actionable advice for the following plant care situation:

PLANT INFORMATION:
- Plant: Chili Pepper (Capsicum annuum)
- Current Growth Stage: vegetative
- Location: indoor

CURRENT CONDITIONS:
- Temperature: 25.5°C
- Humidity: 65.0%
- Soil Moisture: 70.0%
- Light Intensity: 800 lux
- Soil pH: 6.5

OPTIMAL CONDITIONS FOR VEGETATIVE STAGE:
- Temperature: 18-28°C (optimal: 23°C)
- Humidity: 60-80% (optimal: 70%)
- Soil Moisture: 50-70% (optimal: 60%)
- Light Intensity: 400-800 lux (optimal: 600 lux)
- Soil pH: 6.0-7.0 (optimal: 6.5)

USER'S QUESTION: Why are my leaves turning yellow?

Please provide:
1. Direct answer to the user's question
2. Analysis of current conditions vs optimal conditions
3. Specific recommendations for improvement
4. Potential issues to watch for
5. Next steps for plant care

Keep the advice practical, specific to this plant type and growth stage, and easy to follow for a home gardener.
```

## Error Handling

### API Unavailable
When DeepSeek API is unavailable, the system provides fallback advice:

```json
{
  "success": true,
  "advice": "I'm sorry, but I'm currently unable to access AI-powered advice...",
  "plant_type": "chili_pepper",
  "timestamp": "2024-01-15T10:30:00Z",
  "ai_available": false
}
```

### Validation Errors
- Invalid plant type: Returns 400 error with valid options
- Missing required fields: Returns 400 error with missing field names
- Plant not found: Returns 404 error

### Rate Limiting
- Automatic retry with exponential backoff
- Maximum 3 retry attempts
- Graceful degradation to fallback advice

## Testing

### Run Integration Tests

```bash
python test_deepseek_integration.py
```

### Test Without API Key

The system works without an API key, providing fallback advice for testing.

### Test with API Key

```bash
export DEEPSEEK_API_KEY="your-key-here"
python test_deepseek_integration.py
```

## Mobile App Integration

### Request Format for Mobile Apps

```json
{
  "plant_type": "chili_pepper",
  "current_conditions": {
    "temperature": 25.5,
    "humidity": 65.0,
    "soil_moisture": 70.0,
    "light_intensity": 800.0,
    "soil_ph": 6.5,
    "growth_stage": "vegetative",
    "location": "indoor"
  },
  "user_question": "Why are my leaves turning yellow?"
}
```

### Response Handling

```javascript
// Example mobile app response handling
const response = await fetch('/plants/ai-advice', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(requestData)
});

const data = await response.json();

if (data.success) {
  displayAdvice(data.advice);
  if (!data.ai_available) {
    showFallbackMessage();
  }
} else {
  showError(data.detail);
}
```

## Performance Considerations

- **Response Time**: 2-5 seconds for AI responses
- **Fallback Time**: < 1 second for fallback advice
- **Rate Limiting**: 1 request per second to DeepSeek API
- **Caching**: Consider implementing response caching for common questions

## Security

- **API Key**: Store securely in environment variables
- **Input Validation**: All inputs validated and sanitized
- **Rate Limiting**: Prevents API abuse
- **Error Logging**: Comprehensive logging without exposing sensitive data

## Troubleshooting

### Common Issues

1. **"DeepSeek API key not available"**
   - Run `python setup_env.py` to configure environment
   - Edit `.env` file and set your actual API key
   - Restart the server after setting the variable

2. **"Plant not found"**
   - Use valid plant types: `chili_pepper`, `grapevine`, `olive_tree`
   - Check plant database is loaded correctly

3. **"Missing required condition"**
   - Include all required sensor readings in `current_conditions`
   - Check field names match exactly

4. **Rate limiting errors**
   - Wait a few seconds before retrying
   - Consider implementing request queuing

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger('plant_analysis.deepseek_client').setLevel(logging.DEBUG)
```

## Future Enhancements

- **Response Caching**: Cache common questions and answers
- **Multi-Language Support**: Support for different languages
- **Image Analysis**: Analyze plant photos for disease detection
- **Historical Advice**: Track and learn from user feedback
- **Expert Mode**: More detailed technical advice for advanced users
