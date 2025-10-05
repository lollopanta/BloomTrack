"""
DeepSeek AI Client for BloomTracker Plant Analysis System.

This module provides AI-powered gardening advice using DeepSeek API,
integrating plant knowledge base with current sensor data and user questions.
"""

import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from aiohttp import ClientTimeout, ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class DeepSeekClient:
    """
    Client for communicating with DeepSeek AI API for plant care advice.
    
    This class handles API authentication, request formatting, response parsing,
    and error handling for AI-powered gardening recommendations.
    """
    
    def __init__(self):
        """Initialize the DeepSeek client with API configuration."""
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.timeout = ClientTimeout(total=30)
        self.max_retries = 3
        self.rate_limit_delay = 1.0  # seconds
        
        if not self.api_key:
            logger.warning("DEEPSEEK_API_KEY not found in environment variables")
    
    def _is_available(self) -> bool:
        """Check if DeepSeek API is available."""
        return self.api_key is not None
    
    def _create_prompt(self, plant_data: Dict[str, Any], current_conditions: Dict[str, Any], 
                      user_question: str) -> str:
        """
        Create an intelligent prompt combining plant knowledge with current conditions.
        
        Args:
            plant_data: Plant database information
            current_conditions: Current sensor readings
            user_question: User's specific question
            
        Returns:
            Formatted prompt for DeepSeek API
        """
        plant_name = plant_data.get('name', 'Unknown Plant')
        scientific_name = plant_data.get('scientific_name', '')
        growth_stage = current_conditions.get('growth_stage', 'unknown')
        
        # Get optimal conditions for current growth stage
        optimal_conditions = plant_data.get('growth_stages', {}).get(growth_stage, {})
        
        # Format current conditions
        current_temp = current_conditions.get('temperature', 0)
        current_humidity = current_conditions.get('humidity', 0)
        current_moisture = current_conditions.get('soil_moisture', 0)
        current_light = current_conditions.get('light_intensity', 0)
        current_ph = current_conditions.get('soil_ph', 0)
        location = current_conditions.get('location', 'unknown')
        
        # Format optimal conditions
        optimal_temp = optimal_conditions.get('temperature', {})
        optimal_humidity = optimal_conditions.get('humidity', {})
        optimal_moisture = optimal_conditions.get('soil_moisture', {})
        optimal_light = optimal_conditions.get('light_intensity', {})
        optimal_ph = optimal_conditions.get('soil_ph', {})
        
        prompt = f"""You are an expert horticulturist and plant care specialist. Provide detailed, actionable advice for the following plant care situation:

PLANT INFORMATION:
- Plant: {plant_name} ({scientific_name})
- Current Growth Stage: {growth_stage}
- Location: {location}

CURRENT CONDITIONS:
- Temperature: {current_temp}°C
- Humidity: {current_humidity}%
- Soil Moisture: {current_moisture}%
- Light Intensity: {current_light} lux
- Soil pH: {current_ph}

OPTIMAL CONDITIONS FOR {growth_stage.upper()} STAGE:
- Temperature: {optimal_temp.get('min', 'N/A')}-{optimal_temp.get('max', 'N/A')}°C (optimal: {optimal_temp.get('optimal', 'N/A')}°C)
- Humidity: {optimal_humidity.get('min', 'N/A')}-{optimal_humidity.get('max', 'N/A')}% (optimal: {optimal_humidity.get('optimal', 'N/A')}%)
- Soil Moisture: {optimal_moisture.get('min', 'N/A')}-{optimal_moisture.get('max', 'N/A')}% (optimal: {optimal_moisture.get('optimal', 'N/A')}%)
- Light Intensity: {optimal_light.get('min', 'N/A')}-{optimal_light.get('max', 'N/A')} lux (optimal: {optimal_light.get('optimal', 'N/A')} lux)
- Soil pH: {optimal_ph.get('min', 'N/A')}-{optimal_ph.get('max', 'N/A')} (optimal: {optimal_ph.get('optimal', 'N/A')})

USER'S QUESTION: {user_question}

Please provide:
1. Direct answer to the user's question
2. Analysis of current conditions vs optimal conditions
3. Specific recommendations for improvement
4. Potential issues to watch for
5. Next steps for plant care

Keep the advice practical, specific to this plant type and growth stage, and easy to follow for a home gardener."""

        return prompt
    
    async def _make_request(self, prompt: str) -> Optional[str]:
        """
        Make API request to DeepSeek with retry logic and error handling.
        
        Args:
            prompt: Formatted prompt for AI
            
        Returns:
            AI response text or None if failed
        """
        if not self._is_available():
            logger.error("DeepSeek API key not available")
            return None
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(timeout=self.timeout) as session:
                    async with session.post(self.base_url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            ai_response = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                            
                            if ai_response:
                                logger.info(f"DeepSeek API request successful (attempt {attempt + 1})")
                                return ai_response.strip()
                            else:
                                logger.warning(f"Empty response from DeepSeek API (attempt {attempt + 1})")
                                
                        elif response.status == 429:  # Rate limited
                            wait_time = self.rate_limit_delay * (2 ** attempt)
                            logger.warning(f"Rate limited, waiting {wait_time}s before retry {attempt + 1}")
                            await asyncio.sleep(wait_time)
                            continue
                            
                        else:
                            error_text = await response.text()
                            logger.error(f"DeepSeek API error {response.status}: {error_text}")
                            
            except ClientError as e:
                logger.error(f"Network error on attempt {attempt + 1}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.rate_limit_delay * (attempt + 1))
                    
            except asyncio.TimeoutError:
                logger.error(f"Request timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.rate_limit_delay)
                    
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
                break
        
        logger.error("All DeepSeek API attempts failed")
        return None
    
    async def get_gardening_advice(self, plant_data: Dict[str, Any], 
                                 current_conditions: Dict[str, Any], 
                                 user_question: str) -> str:
        """
        Get AI-powered gardening advice for a specific plant and situation.
        
        Args:
            plant_data: Plant database information
            current_conditions: Current sensor readings
            user_question: User's specific question
            
        Returns:
            AI-generated gardening advice
        """
        try:
            logger.info(f"Generating AI advice for {plant_data.get('name', 'Unknown')} plant")
            
            # Create intelligent prompt
            prompt = self._create_prompt(plant_data, current_conditions, user_question)
            
            # Make API request
            ai_response = await self._make_request(prompt)
            
            if ai_response:
                logger.info("AI advice generated successfully")
                return ai_response
            else:
                # Fallback response when AI is unavailable
                return self._get_fallback_advice(plant_data, current_conditions, user_question)
                
        except Exception as e:
            logger.error(f"Error generating AI advice: {str(e)}")
            return self._get_fallback_advice(plant_data, current_conditions, user_question)
    
    def _get_fallback_advice(self, plant_data: Dict[str, Any], 
                           current_conditions: Dict[str, Any], 
                           user_question: str) -> str:
        """
        Provide fallback advice when AI is unavailable.
        
        Args:
            plant_data: Plant database information
            current_conditions: Current sensor readings
            user_question: User's specific question
            
        Returns:
            Basic fallback advice
        """
        plant_name = plant_data.get('name', 'your plant')
        growth_stage = current_conditions.get('growth_stage', 'current stage')
        
        # Basic condition analysis
        temp = current_conditions.get('temperature', 0)
        humidity = current_conditions.get('humidity', 0)
        moisture = current_conditions.get('soil_moisture', 0)
        ph = current_conditions.get('soil_ph', 0)
        
        advice_parts = [
            f"I'm sorry, but I'm currently unable to access AI-powered advice for your {plant_name}.",
            f"However, here's some basic guidance for your {growth_stage} plant:",
            "",
            "CURRENT CONDITIONS ANALYSIS:",
            f"• Temperature: {temp}°C",
            f"• Humidity: {humidity}%",
            f"• Soil Moisture: {moisture}%",
            f"• Soil pH: {ph}",
            "",
            "GENERAL RECOMMENDATIONS:",
            "• Ensure consistent watering schedule",
            "• Monitor for signs of over/under-watering",
            "• Check for pests and diseases regularly",
            "• Provide adequate light for the growth stage",
            "• Maintain proper soil pH levels",
            "",
            "For more specific advice, please try again later or consult a local gardening expert.",
            "",
            f"Your question: '{user_question}' - This will be addressed when AI services are restored."
        ]
        
        return "\n".join(advice_parts)
    
    async def test_connection(self) -> bool:
        """
        Test DeepSeek API connection and authentication.
        
        Returns:
            True if connection successful, False otherwise
        """
        if not self._is_available():
            return False
        
        try:
            test_prompt = "Hello, please respond with 'Connection successful' to test the API."
            response = await self._make_request(test_prompt)
            return response is not None and "successful" in response.lower()
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

# Global instance
deepseek_client = DeepSeekClient()
