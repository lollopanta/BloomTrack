#!/usr/bin/env python3
"""
BloomTrack Advanced API Test Script
Test the new advanced geospatial and ML features
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def test_advanced_endpoint(endpoint, description, method="GET", params=None, data=None):
    """Test an advanced API endpoint"""
    print(f"\nTesting: {description}")
    print(f"Endpoint: {endpoint}")
    if params:
        print(f"Parameters: {params}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        elif method.upper() == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS! Status: {response.status_code}")
            print(f"Response type: {type(data)}")
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
            elif isinstance(data, list):
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
    """Run all advanced API tests"""
    print("BloomTrack Advanced API Test Suite")
    print("=" * 60)
    
    # Test geospatial analysis endpoints
    print("\n" + "="*30)
    print("GEOSPATIAL ANALYSIS TESTS")
    print("="*30)
    
    geo_tests = [
        ("/api/analysis/spatial-clusters", "Spatial Clustering", {"eps": 0.5, "min_samples": 2}),
        ("/api/analysis/bloom-density", "Bloom Density Analysis", {"grid_size": 1.0}),
        ("/api/analysis/temporal-patterns", "Temporal Pattern Analysis"),
        ("/api/analysis/spatial-statistics", "Spatial Statistics"),
    ]
    
    geo_results = []
    for endpoint, description, *params in geo_tests:
        param_dict = params[0] if params else None
        result = test_advanced_endpoint(endpoint, description, params=param_dict)
        geo_results.append(result)
    
    # Test map endpoints
    print("\n" + "="*30)
    print("INTERACTIVE MAP TESTS")
    print("="*30)
    
    map_tests = [
        ("/api/maps/interactive", "Interactive Map", {"center_lat": 40.0, "center_lon": -100.0, "zoom": 4}),
        ("/api/maps/conservation-priority", "Conservation Priority Map"),
    ]
    
    map_results = []
    for endpoint, description, *params in map_tests:
        param_dict = params[0] if params else None
        result = test_advanced_endpoint(endpoint, description, params=param_dict)
        map_results.append(result)
    
    # Test export endpoints
    print("\n" + "="*30)
    print("DATA EXPORT TESTS")
    print("="*30)
    
    export_tests = [
        ("/api/export/spatial-data", "Export GeoJSON", {"format": "geojson"}),
        ("/api/export/spatial-data", "Export CSV", {"format": "csv"}),
    ]
    
    export_results = []
    for endpoint, description, params in export_tests:
        result = test_advanced_endpoint(endpoint, description, params=params)
        export_results.append(result)
    
    # Test ML endpoints
    print("\n" + "="*30)
    print("MACHINE LEARNING TESTS")
    print("="*30)
    
    # Train models first
    ml_train_tests = [
        ("/api/ml/train-intensity-model", "Train Intensity Model", "POST"),
        ("/api/ml/train-timing-model", "Train Timing Model", "POST"),
    ]
    
    ml_train_results = []
    for endpoint, description, method in ml_train_tests:
        result = test_advanced_endpoint(endpoint, description, method=method)
        ml_train_results.append(result)
    
    # Test ML predictions
    ml_prediction_tests = [
        ("/api/ml/predict-intensity", "Predict Bloom Intensity", {
            "lat": 36.7783, "lon": -119.4179, "date": "2024-06-15", 
            "vegetation_type": "agricultural", "area_coverage": 500.0
        }),
        ("/api/ml/predict-timing", "Predict Bloom Timing", {
            "lat": 40.7128, "lon": -74.0060, "vegetation_type": "forest"
        }),
        ("/api/ml/analyze-anomalies", "Analyze Bloom Anomalies"),
        ("/api/ml/forecast", "Generate Bloom Forecast", {"months": 6}),
    ]
    
    ml_prediction_results = []
    for endpoint, description, *params in ml_prediction_tests:
        param_dict = params[0] if params else None
        result = test_advanced_endpoint(endpoint, description, params=param_dict)
        ml_prediction_results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("ADVANCED API TEST RESULTS SUMMARY")
    print("=" * 60)
    
    geo_passed = sum(geo_results)
    geo_total = len(geo_results)
    map_passed = sum(map_results)
    map_total = len(map_results)
    export_passed = sum(export_results)
    export_total = len(export_results)
    ml_train_passed = sum(ml_train_results)
    ml_train_total = len(ml_train_results)
    ml_prediction_passed = sum(ml_prediction_results)
    ml_prediction_total = len(ml_prediction_results)
    
    total_passed = geo_passed + map_passed + export_passed + ml_train_passed + ml_prediction_passed
    total_tests = geo_total + map_total + export_total + ml_train_total + ml_prediction_total
    
    print(f"Geospatial Analysis: {geo_passed}/{geo_total} passed")
    print(f"Interactive Maps: {map_passed}/{map_total} passed")
    print(f"Data Export: {export_passed}/{export_total} passed")
    print(f"ML Model Training: {ml_train_passed}/{ml_train_total} passed")
    print(f"ML Predictions: {ml_prediction_passed}/{ml_prediction_total} passed")
    print(f"Overall: {total_passed}/{total_tests} passed")
    
    if total_passed == total_tests:
        print("\nAll advanced tests passed! BloomTrack is fully operational!")
        print("\nAdvanced Features Available:")
        print("- Spatial clustering and density analysis")
        print("- Interactive maps with satellite imagery")
        print("- Machine learning bloom prediction")
        print("- Data export in multiple formats")
        print("- Conservation priority mapping")
        print("- Temporal pattern analysis")
    else:
        print(f"\n{total_tests - total_passed} tests failed. Check the server logs.")
    
    print("\nVisit http://localhost:8000/api/docs for full API documentation!")
    print("Advanced features are now available for bloom monitoring and analysis!")

if __name__ == "__main__":
    main()

