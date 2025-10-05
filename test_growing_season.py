#!/usr/bin/env python3
"""
Test script for growing season AI responses
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_growing_season_question():
    """Test AI response to growing season question"""
    
    print("🌱 Testing Growing Season AI Response")
    print("=" * 50)
    
    # Test growing season question for chili pepper
    print("\n🌶️ Testing Chili Pepper Growing Season Question")
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
            print(f"   AI Response: {data['advice']}")
            print(f"   Health Score: {data['health_score']}/100")
            print(f"   Success: {data['success']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test growing season question for grapevine
    print("\n🍇 Testing Grapevine Growing Season Question")
    try:
        ai_request = {
            "plant_type": "grapevine",
            "current_conditions": {
                "temperature": 25.0,
                "humidity": 45.0,
                "soil_moisture": 55.0,
                "light_intensity": 12000.0,
                "soil_ph": 6.8,
                "growth_stage": "vegetative",
                "location": "outdoor"
            },
            "user_question": "When should I plant my grapevine?",
            "chat_history": []
        }
        
        response = requests.post(f"{BASE_URL}/plants/grapevine/ai-advice", json=ai_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   AI Response: {data['advice']}")
            print(f"   Health Score: {data['health_score']}/100")
            print(f"   Success: {data['success']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test growing season question for olive tree
    print("\n🫒 Testing Olive Tree Growing Season Question")
    try:
        ai_request = {
            "plant_type": "olive_tree",
            "current_conditions": {
                "temperature": 25.0,
                "humidity": 35.0,
                "soil_moisture": 45.0,
                "light_intensity": 15000.0,
                "soil_ph": 7.2,
                "growth_stage": "vegetative",
                "location": "outdoor"
            },
            "user_question": "What are the best months to grow olive trees?",
            "chat_history": []
        }
        
        response = requests.post(f"{BASE_URL}/plants/olive_tree/ai-advice", json=ai_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   AI Response: {data['advice']}")
            print(f"   Health Score: {data['health_score']}/100")
            print(f"   Success: {data['success']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Growing season AI test completed!")
    print("\n📱 Access the web interface at: http://localhost:3000/plant-ai")
    print("🔗 API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    test_growing_season_question()
