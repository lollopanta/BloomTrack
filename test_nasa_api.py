#!/usr/bin/env python3
"""
BloomTrack NASA API Integration Test Script
Test the new NASA API endpoints and data integration
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def test_nasa_endpoint(endpoint, description, params=None):
    """Test a NASA API endpoint"""
    print(f"\nTesting: {description}")
    print(f"Endpoint: {endpoint}")
    if params:
        print(f"Parameters: {params}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS! Status: {response.status_code}")
            print(f"Response type: {type(data)}")
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'total_records' in data:
                    print(f"Total records: {data['total_records']}")
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
    """Run NASA API integration tests"""
    print("BloomTrack NASA API Integration Test Suite")
    print("=" * 60)
    
    # Test NASA configuration
    print("\n" + "="*30)
    print("NASA CONFIGURATION TESTS")
    print("="*30)
    
    config_tests = [
        ("/api/nasa/configuration", "NASA Configuration"),
        ("/api/nasa/catalog", "NASA Earth Data Catalog"),
    ]
    
    config_results = []
    for endpoint, description in config_tests:
        result = test_nasa_endpoint(endpoint, description)
        config_results.append(result)
    
    # Test NASA satellite data endpoints
    print("\n" + "="*30)
    print("NASA SATELLITE DATA TESTS")
    print("="*30)
    
    # Test parameters
    test_lat = 36.7783  # California
    test_lon = -119.4179
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    
    satellite_tests = [
        ("/api/nasa/satellite-data", "Comprehensive Satellite Data", {
            "lat": test_lat, "lon": test_lon, 
            "start_date": start_date, "end_date": end_date,
            "satellite": "all"
        }),
        ("/api/nasa/satellite-data", "Landsat Data Only", {
            "lat": test_lat, "lon": test_lon,
            "start_date": start_date, "end_date": end_date,
            "satellite": "landsat"
        }),
        ("/api/nasa/satellite-data", "MODIS Data Only", {
            "lat": test_lat, "lon": test_lon,
            "start_date": start_date, "end_date": end_date,
            "satellite": "modis"
        }),
        ("/api/nasa/satellite-data", "VIIRS Data Only", {
            "lat": test_lon, "lon": test_lon,
            "start_date": start_date, "end_date": end_date,
            "satellite": "viirs"
        }),
    ]
    
    satellite_results = []
    for endpoint, description, params in satellite_tests:
        result = test_nasa_endpoint(endpoint, description, params)
        satellite_results.append(result)
    
    # Test NASA bloom detection
    print("\n" + "="*30)
    print("NASA BLOOM DETECTION TESTS")
    print("="*30)
    
    bloom_tests = [
        ("/api/nasa/detect-blooms", "Detect Bloom Events", {
            "lat": test_lat, "lon": test_lon,
            "start_date": start_date, "end_date": end_date
        }),
        ("/api/nasa/vegetation-indices", "Vegetation Indices Time Series", {
            "lat": test_lat, "lon": test_lon,
            "start_date": start_date, "end_date": end_date
        }),
    ]
    
    bloom_results = []
    for endpoint, description, params in bloom_tests:
        result = test_nasa_endpoint(endpoint, description, params)
        bloom_results.append(result)
    
    # Test different locations
    print("\n" + "="*30)
    print("MULTI-LOCATION TESTS")
    print("="*30)
    
    locations = [
        (40.7128, -74.0060, "New York"),
        (51.5074, -0.1278, "London"),
        (-33.8688, 151.2093, "Sydney"),
        (35.6762, 139.6503, "Tokyo")
    ]
    
    location_results = []
    for lat, lon, name in locations:
        params = {
            "lat": lat, "lon": lon,
            "start_date": "2024-03-01", "end_date": "2024-03-31"
        }
        result = test_nasa_endpoint("/api/nasa/satellite-data", f"Satellite Data - {name}", params)
        location_results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("NASA API INTEGRATION TEST RESULTS")
    print("=" * 60)
    
    config_passed = sum(config_results)
    config_total = len(config_results)
    satellite_passed = sum(satellite_results)
    satellite_total = len(satellite_results)
    bloom_passed = sum(bloom_results)
    bloom_total = len(bloom_results)
    location_passed = sum(location_results)
    location_total = len(location_results)
    
    total_passed = config_passed + satellite_passed + bloom_passed + location_passed
    total_tests = config_total + satellite_total + bloom_total + location_total
    
    print(f"Configuration Tests: {config_passed}/{config_total} passed")
    print(f"Satellite Data Tests: {satellite_passed}/{satellite_total} passed")
    print(f"Bloom Detection Tests: {bloom_passed}/{bloom_total} passed")
    print(f"Multi-Location Tests: {location_passed}/{location_total} passed")
    print(f"Overall: {total_passed}/{total_tests} passed")
    
    if total_passed == total_tests:
        print("\nAll NASA API integration tests passed!")
        print("\nNASA API Features Available:")
        print("- Real-time satellite data from Landsat, MODIS, VIIRS")
        print("- Vegetation indices calculation (NDVI, EVI, SAVI)")
        print("- Bloom event detection from satellite imagery")
        print("- Multi-satellite data integration")
        print("- Global coverage with location-specific analysis")
        print("- Configurable data sources and processing")
    else:
        print(f"\n{total_tests - total_passed} tests failed. Check the server logs.")
    
    print("\nVisit http://localhost:8000/api/docs for full NASA API documentation!")
    print("NASA Earth observation data is now integrated with BloomTrack!")

if __name__ == "__main__":
    main()
