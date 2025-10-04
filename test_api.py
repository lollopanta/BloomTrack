#!/usr/bin/env python3
"""
BloomTrack API Test Script
Simple script to test the API endpoints and verify functionality
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, description):
    """Test a single API endpoint"""
    print(f"\nTesting: {description}")
    print(f"Endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS! Status: {response.status_code}")
            print(f"Response type: {type(data)}")
            if isinstance(data, list):
                print(f"Number of items: {len(data)}")
            elif isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
            return True
        else:
            print(f"ERROR! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Connection Error! Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def test_parameterized_endpoint(endpoint, params, description):
    """Test an endpoint with query parameters"""
    print(f"\nTesting: {description}")
    print(f"Endpoint: {endpoint}")
    print(f"Parameters: {params}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS! Status: {response.status_code}")
            print(f"Response type: {type(data)}")
            if isinstance(data, list):
                print(f"Number of items: {len(data)}")
            return True
        else:
            print(f"ERROR! Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Connection Error! Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Run all API tests"""
    print("BloomTrack API Test Suite")
    print("=" * 50)
    
    # Test basic endpoints
    tests = [
        ("/api/health", "Health Check"),
        ("/api/bloom-events", "Get All Bloom Events"),
        ("/api/statistics/global", "Global Statistics"),
    ]
    
    # Test parameterized endpoints
    param_tests = [
        ("/api/bloom-events", {"region": "North America"}, "Filter by Region"),
        ("/api/bloom-events", {"intensity": "high"}, "Filter by Intensity"),
        ("/api/satellite-data", {
            "lat": 36.7783, 
            "lon": -119.4179, 
            "start_date": "2024-01-01", 
            "end_date": "2024-12-31"
        }, "Satellite Data for California"),
        ("/api/bloom-detection", {
            "lat": 36.7783, 
            "lon": -119.4179, 
            "radius": 50
        }, "Bloom Detection in California"),
        ("/api/visualization/heatmap", {"region": "North America"}, "North America Heatmap"),
    ]
    
    # Run basic tests
    print("\nRunning Basic Endpoint Tests...")
    basic_results = []
    for endpoint, description in tests:
        result = test_endpoint(endpoint, description)
        basic_results.append(result)
    
    # Run parameterized tests
    print("\nRunning Parameterized Endpoint Tests...")
    param_results = []
    for endpoint, params, description in param_tests:
        result = test_parameterized_endpoint(endpoint, params, description)
        param_results.append(result)
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    basic_passed = sum(basic_results)
    basic_total = len(basic_results)
    param_passed = sum(param_results)
    param_total = len(param_results)
    
    print(f"Basic Tests: {basic_passed}/{basic_total} passed")
    print(f"Parameterized Tests: {param_passed}/{param_total} passed")
    print(f"Overall: {basic_passed + param_passed}/{basic_total + param_total} passed")
    
    if basic_passed + param_passed == basic_total + param_total:
        print("\nAll tests passed! BloomTrack API is working correctly!")
    else:
        print(f"\n{basic_total + param_total - basic_passed - param_passed} tests failed. Check the server logs.")
    
    print("\nVisit http://localhost:8000 to see the BloomTrack dashboard!")
    print("API Documentation: http://localhost:8000/api/docs")

if __name__ == "__main__":
    main()
