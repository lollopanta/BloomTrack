#!/usr/bin/env python3
"""
Test script for Plant AI Advisor endpoints
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_plant_ai_endpoints():
    """Test all Plant AI Advisor endpoints"""
    
    print("🌱 Testing Plant AI Advisor Endpoints")
    print("=" * 50)
    
    # Test 1: Get optimal ranges for chili pepper
    print("\n1. Testing GET /plants/chili_pepper/optimal-ranges")
    try:
        response = requests.get(f"{BASE_URL}/plants/chili_pepper/optimal-ranges")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   Plant: {data['plant_name']}")
            print(f"   Temperature range: {data['optimal_conditions']['temperature']}")
            print(f"   Growth stages: {data['growth_stages']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 2: Analyze plant conditions
    print("\n2. Testing POST /plants/chili_pepper/analyze")
    try:
        sensor_data = {
            "temperature": 25.5,
            "humidity": 65.0,
            "soil_moisture": 70.0,
            "light_intensity": 8000.0,
            "soil_ph": 6.5,
            "growth_stage": "vegetative",
            "location": "indoor"
        }
        
        response = requests.post(f"{BASE_URL}/plants/chili_pepper/analyze", json=sensor_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   Health Score: {data['health_score']}/100")
            print(f"   Critical Issues: {data['critical_issues']}")
            print(f"   Recommendations: {data['recommendations']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 3: Get AI advice
    print("\n3. Testing POST /plants/chili_pepper/ai-advice")
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
            "user_question": "Why are my leaves turning yellow?",
            "chat_history": []
        }
        
        response = requests.post(f"{BASE_URL}/plants/chili_pepper/ai-advice", json=ai_request)
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   AI Advice: {data['advice'][:100]}...")
            print(f"   Health Score: {data['health_score']}/100")
            print(f"   Success: {data['success']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 4: Get health score
    print("\n4. Testing POST /plants/chili_pepper/health-score")
    try:
        sensor_data = {
            "temperature": 25.5,
            "humidity": 65.0,
            "soil_moisture": 70.0,
            "light_intensity": 8000.0,
            "soil_ph": 6.5,
            "growth_stage": "vegetative",
            "location": "indoor"
        }
        
        response = requests.post(f"{BASE_URL}/plants/chili_pepper/health-score", json=sensor_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"   Health Score: {data['health_score']}/100")
            print(f"   Parameter Scores: {data['parameter_scores']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Plant AI Advisor endpoints test completed!")
    print("\n📱 Access the web interface at: http://localhost:3000/plant-ai")
    print("🔗 API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    test_plant_ai_endpoints()
