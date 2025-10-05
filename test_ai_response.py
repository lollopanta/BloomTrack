#!/usr/bin/env python3
"""
Test AI response content
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_ai_response_content():
    """Test what the AI response actually contains"""
    
    print("🔍 Testing AI Response Content")
    print("=" * 50)
    
    # Test AI advice for chili pepper
    try:
        ai_request = {
            "plant_type": "chili_pepper",
            "current_conditions": {
                "temperature": 25.5,
                "humidity": 65.0,
                "soil_moisture": 70.0,
                "light_intensity": 8000.0,
                "soil_ph": 6.5,
                "growth_stage": "vegetative",
                "location": "indoor"
            },
            "user_question": "What is the growing season for this plant?",
            "chat_history": []
        }
        
        response = requests.post(f"{BASE_URL}/plants/chili_pepper/ai-advice", json=ai_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   Full Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_ai_response_content()
