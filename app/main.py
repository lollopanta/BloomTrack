from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime, timedelta
import json
import os

from app.models.plant_models import PlantBloomEvent, SatelliteData, BloomDetection
from app.services.data_processor import DataProcessor
from app.services.nasa_data_service import NASADataService
from app.services.visualization_service import VisualizationService
from app.services.geospatial_analyzer import GeospatialAnalyzer
from app.services.ml_predictor import MLBloomPredictor
from app.services.nasa_api_integration import NASAAPIIntegration
from app.core.config import get_settings, load_env_file

# Load environment configuration
load_env_file()

# Get application settings
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Plant Blooming Event Monitoring System using NASA Earth Observation Data",
    version=settings.version,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
data_processor = DataProcessor()
nasa_service = NASADataService()
viz_service = VisualizationService()
geo_analyzer = GeospatialAnalyzer()
ml_predictor = MLBloomPredictor()
nasa_api = NASAAPIIntegration()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BloomTrack - Plant Blooming Monitor</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .hero-gradient {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .card-hover:hover {
                transform: translateY(-5px);
                transition: transform 0.3s ease;
            }
            .bloom-indicator {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                display: inline-block;
                margin-right: 8px;
            }
            .bloom-high { background-color: #ff6b6b; }
            .bloom-medium { background-color: #ffa726; }
            .bloom-low { background-color: #66bb6a; }
        </style>
    </head>
    <body>
        <section class="hero hero-gradient is-medium">
            <div class="hero-body">
                <div class="container">
                    <h1 class="title is-1 has-text-white">
                        <i class="fas fa-seedling"></i> BloomTrack
                    </h1>
                    <h2 class="subtitle is-3 has-text-white">
                        Monitor Plant Blooming Events Across the Globe
                    </h2>
                    <p class="has-text-white">
                        Harnessing NASA Earth observation data to track vegetation changes and blooming events worldwide
                    </p>
                    <div class="buttons mt-4">
                        <a class="button is-white" href="/advanced">
                            <span class="icon"><i class="fas fa-rocket"></i></span>
                            <span>Advanced Features</span>
                        </a>
                        <a class="button is-white is-outlined" href="/data-management">
                            <span class="icon"><i class="fas fa-database"></i></span>
                            <span>Data Management</span>
                        </a>
                        <a class="button is-white is-outlined" href="/api/docs">
                            <span class="icon"><i class="fas fa-book"></i></span>
                            <span>API Documentation</span>
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="columns is-multiline" id="bloom-cards">
                    <!-- Bloom event cards will be loaded here -->
                </div>
                
            <div class="has-text-centered" style="margin-top: 2rem;">
                <button class="button is-primary is-large" onclick="loadBloomData()">
                    <span class="icon">
                        <i class="fas fa-satellite"></i>
                    </span>
                    <span>Load Global Bloom Data</span>
                </button>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="section has-background-light">
        <div class="container">
            <h2 class="title is-2 has-text-centered">BloomTrack Features</h2>
            <div class="columns is-multiline">
                <div class="column is-one-third">
                    <div class="card card-hover">
                        <div class="card-content has-text-centered">
                            <i class="fas fa-globe fa-3x has-text-primary"></i>
                            <h3 class="title is-4 mt-3">Global Monitoring</h3>
                            <p>Track bloom events across the globe using NASA satellite data</p>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="card card-hover">
                        <div class="card-content has-text-centered">
                            <i class="fas fa-brain fa-3x has-text-success"></i>
                            <h3 class="title is-4 mt-3">AI Predictions</h3>
                            <p>Machine learning models for bloom intensity and timing predictions</p>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="card card-hover">
                        <div class="card-content has-text-centered">
                            <i class="fas fa-map-marked-alt fa-3x has-text-info"></i>
                            <h3 class="title is-4 mt-3">Geospatial Analysis</h3>
                            <p>Advanced spatial clustering and density analysis</p>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="card card-hover">
                        <div class="card-content has-text-centered">
                            <i class="fas fa-chart-line fa-3x has-text-warning"></i>
                            <h3 class="title is-4 mt-3">Temporal Analysis</h3>
                            <p>Seasonal patterns and trend analysis</p>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="card card-hover">
                        <div class="card-content has-text-centered">
                            <i class="fas fa-download fa-3x has-text-danger"></i>
                            <h3 class="title is-4 mt-3">Data Export</h3>
                            <p>Export data in GeoJSON, CSV, and KML formats</p>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="card card-hover">
                        <div class="card-content has-text-centered">
                            <i class="fas fa-shield-alt fa-3x has-text-link"></i>
                            <h3 class="title is-4 mt-3">Conservation</h3>
                            <p>Priority mapping for conservation efforts</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Quick Actions Section -->
    <section class="section">
        <div class="container">
            <h2 class="title is-2 has-text-centered">Quick Actions</h2>
            <div class="columns">
                <div class="column is-half">
                    <div class="card">
                        <div class="card-content">
                            <h3 class="title is-4">Data Management</h3>
                            <p>Add new bloom events, filter data, and export results</p>
                            <a class="button is-primary" href="/data-management">
                                <span class="icon"><i class="fas fa-database"></i></span>
                                <span>Manage Data</span>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="column is-half">
                    <div class="card">
                        <div class="card-content">
                            <h3 class="title is-4">Advanced Analysis</h3>
                            <p>Run spatial clustering, ML predictions, and generate maps</p>
                            <a class="button is-success" href="/advanced">
                                <span class="icon"><i class="fas fa-rocket"></i></span>
                                <span>Advanced Features</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            </div>
        </section>

        <script>
            async function loadBloomData() {
                const button = document.querySelector('button');
                button.classList.add('is-loading');
                
                try {
                    const response = await fetch('/api/bloom-events');
                    const data = await response.json();
                    displayBloomCards(data);
                } catch (error) {
                    console.error('Error loading bloom data:', error);
                    alert('Error loading bloom data. Please try again.');
                } finally {
                    button.classList.remove('is-loading');
                }
            }

            function displayBloomCards(events) {
                const container = document.getElementById('bloom-cards');
                container.innerHTML = '';

                events.forEach(event => {
                    const card = document.createElement('div');
                    card.className = 'column is-one-third';
                    card.innerHTML = `
                        <div class="card card-hover">
                            <div class="card-content">
                                <div class="media">
                                    <div class="media-content">
                                        <p class="title is-4">${event.location}</p>
                                        <p class="subtitle is-6">${event.region}</p>
                                    </div>
                                </div>
                                <div class="content">
                                    <p><strong>Bloom Intensity:</strong> 
                                        <span class="bloom-indicator bloom-${event.intensity.toLowerCase()}"></span>
                                        ${event.intensity}
                                    </p>
                                    <p><strong>Date:</strong> ${new Date(event.detection_date).toLocaleDateString()}</p>
                                    <p><strong>Satellite:</strong> ${event.satellite_source}</p>
                                    <p><strong>Confidence:</strong> ${event.confidence}%</p>
                                    <div class="tags">
                                        <span class="tag is-primary">${event.vegetation_type}</span>
                                        <span class="tag is-info">${event.season}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);
                });
            }

            // Load initial data
            loadBloomData();
        </script>
    </body>
    </html>
    """

@app.get("/advanced", response_class=HTMLResponse)
async def advanced_dashboard():
    """Serve the advanced dashboard page"""
    try:
        with open("app/templates/advanced_dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head><title>BloomTrack Advanced</title></head>
        <body>
            <h1>Advanced Dashboard</h1>
            <p>Advanced features are being loaded...</p>
            <a href="/">Back to Main Dashboard</a>
        </body>
        </html>
        """

@app.get("/data-management", response_class=HTMLResponse)
async def data_management():
    """Serve the data management page"""
    try:
        with open("app/templates/data_management.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head><title>BloomTrack Data Management</title></head>
        <body>
            <h1>Data Management</h1>
            <p>Data management features are being loaded...</p>
            <a href="/">Back to Main Dashboard</a>
        </body>
        </html>
        """

@app.get("/api/bloom-events", response_model=List[PlantBloomEvent])
async def get_bloom_events(
    region: Optional[str] = Query(None, description="Filter by region"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    intensity: Optional[str] = Query(None, description="Filter by bloom intensity (high/medium/low)")
):
    """Get plant blooming events with optional filters"""
    try:
        events = await data_processor.get_bloom_events(
            region=region,
            start_date=start_date,
            end_date=end_date,
            intensity=intensity
        )
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/satellite-data")
async def get_satellite_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)")
):
    """Get satellite data for a specific location and time range"""
    try:
        data = await nasa_service.get_satellite_data(lat, lon, start_date, end_date)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bloom-detection")
async def detect_bloom_events(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius: float = Query(10.0, description="Search radius in kilometers")
):
    """Detect bloom events in a specific area"""
    try:
        detections = await data_processor.detect_bloom_events(lat, lon, radius)
        return detections
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visualization/heatmap")
async def get_bloom_heatmap(
    region: Optional[str] = Query(None, description="Region to visualize"),
    start_date: Optional[str] = Query(None, description="Start date"),
    end_date: Optional[str] = Query(None, description="End date")
):
    """Generate bloom intensity heatmap"""
    try:
        heatmap_data = await viz_service.generate_bloom_heatmap(region, start_date, end_date)
        return heatmap_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/statistics/global")
async def get_global_statistics():
    """Get global bloom statistics"""
    try:
        stats = await data_processor.get_global_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Advanced Geospatial Analysis Endpoints
@app.get("/api/analysis/spatial-clusters")
async def get_spatial_clusters(
    eps: float = Query(0.5, description="DBSCAN epsilon parameter"),
    min_samples: int = Query(2, description="Minimum samples for cluster")
):
    """Detect spatial clusters in bloom events"""
    try:
        events = await data_processor.get_bloom_events()
        clusters = geo_analyzer.detect_bloom_clusters(events, eps, min_samples)
        return clusters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/bloom-density")
async def get_bloom_density(
    grid_size: float = Query(1.0, description="Grid cell size in degrees")
):
    """Calculate bloom density using spatial grid analysis"""
    try:
        events = await data_processor.get_bloom_events()
        density = geo_analyzer.calculate_bloom_density(events, grid_size)
        return density
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/temporal-patterns")
async def get_temporal_patterns():
    """Analyze temporal patterns in bloom events"""
    try:
        events = await data_processor.get_bloom_events()
        patterns = geo_analyzer.analyze_temporal_patterns(events)
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/spatial-statistics")
async def get_spatial_statistics():
    """Get comprehensive spatial statistics"""
    try:
        events = await data_processor.get_bloom_events()
        stats = geo_analyzer.calculate_spatial_statistics(events)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/maps/interactive")
async def get_interactive_map(
    center_lat: float = Query(20.0, description="Map center latitude"),
    center_lon: float = Query(0.0, description="Map center longitude"),
    zoom: int = Query(2, description="Initial zoom level")
):
    """Generate interactive map with bloom events"""
    try:
        events = await data_processor.get_bloom_events()
        map_html = geo_analyzer.create_interactive_map(
            events, (center_lat, center_lon), zoom
        )
        return {"map_html": map_html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/maps/conservation-priority")
async def get_conservation_priority_map():
    """Generate conservation priority map"""
    try:
        events = await data_processor.get_bloom_events()
        map_html = geo_analyzer.generate_conservation_priority_map(events)
        return {"map_html": map_html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/spatial-data")
async def export_spatial_data(
    format: str = Query("geojson", description="Export format (geojson, csv, kml)")
):
    """Export spatial data in various formats"""
    try:
        events = await data_processor.get_bloom_events()
        data = geo_analyzer.export_spatial_data(events, format)
        return {"data": data, "format": format}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Machine Learning Endpoints
@app.post("/api/ml/train-intensity-model")
async def train_intensity_model():
    """Train ML model for bloom intensity prediction"""
    try:
        events = await data_processor.get_bloom_events()
        results = ml_predictor.train_bloom_intensity_model(events)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ml/train-timing-model")
async def train_timing_model():
    """Train ML model for bloom timing prediction"""
    try:
        events = await data_processor.get_bloom_events()
        results = ml_predictor.train_bloom_timing_model(events)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ml/predict-intensity")
async def predict_bloom_intensity(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    date: str = Query(..., description="Date (YYYY-MM-DD)"),
    vegetation_type: str = Query(..., description="Vegetation type"),
    area_coverage: float = Query(100.0, description="Area coverage in km²")
):
    """Predict bloom intensity for given parameters"""
    try:
        prediction_date = datetime.fromisoformat(date)
        prediction = ml_predictor.predict_bloom_intensity(
            lat, lon, prediction_date, vegetation_type, area_coverage
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ml/predict-timing")
async def predict_bloom_timing(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    vegetation_type: str = Query(..., description="Vegetation type"),
    year: int = Query(None, description="Year for prediction")
):
    """Predict bloom timing for given location and vegetation type"""
    try:
        prediction = ml_predictor.predict_bloom_timing(
            lat, lon, vegetation_type, year
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ml/analyze-anomalies")
async def analyze_bloom_anomalies():
    """Analyze anomalies in bloom patterns using ML"""
    try:
        events = await data_processor.get_bloom_events()
        anomalies = ml_predictor.analyze_bloom_anomalies(events)
        return anomalies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ml/forecast")
async def generate_bloom_forecast(
    months: int = Query(6, description="Number of months to forecast")
):
    """Generate bloom forecast for upcoming months"""
    try:
        events = await data_processor.get_bloom_events()
        forecast = ml_predictor.generate_bloom_forecast(events, months)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# NASA API Integration Endpoints
@app.get("/api/nasa/satellite-data")
async def get_nasa_satellite_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    satellite: str = Query("all", description="Satellite source (landsat, modis, viirs, all)")
):
    """Get comprehensive NASA satellite data"""
    try:
        async with nasa_api:
            if satellite == "all":
                data = await nasa_api.get_comprehensive_satellite_data(lat, lon, start_date, end_date)
            elif satellite == "landsat":
                data = await nasa_api.get_landsat_data(lat, lon, start_date, end_date)
            elif satellite == "modis":
                data = await nasa_api.get_modis_data(lat, lon, start_date, end_date)
            elif satellite == "viirs":
                data = await nasa_api.get_viirs_data(lat, lon, start_date, end_date)
            else:
                raise HTTPException(status_code=400, detail="Invalid satellite source")
            
            return {
                "satellite_data": data,
                "total_records": len(data),
                "date_range": {"start": start_date, "end": end_date},
                "location": {"lat": lat, "lon": lon}
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa/detect-blooms")
async def detect_nasa_bloom_events(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)")
):
    """Detect bloom events using NASA satellite data"""
    try:
        async with nasa_api:
            bloom_events = await nasa_api.detect_bloom_events_from_satellite_data(
                lat, lon, start_date, end_date
            )
            return {
                "bloom_events": bloom_events,
                "total_events": len(bloom_events),
                "detection_period": {"start": start_date, "end": end_date},
                "location": {"lat": lat, "lon": lon}
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa/catalog")
async def get_nasa_catalog():
    """Get NASA Earth Data catalog information"""
    try:
        async with nasa_api:
            catalog = await nasa_api.get_nasa_earth_data_catalog()
            return catalog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa/vegetation-indices")
async def get_vegetation_indices(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)")
):
    """Get vegetation indices time series from NASA data"""
    try:
        async with nasa_api:
            satellite_data = await nasa_api.get_comprehensive_satellite_data(lat, lon, start_date, end_date)
            
            # Extract vegetation indices
            indices_data = []
            for data in satellite_data:
                indices_data.append({
                    "date": data.acquisition_date.isoformat(),
                    "satellite": data.satellite.value,
                    "ndvi": data.spectral_data.get("NDVI", 0),
                    "evi": data.spectral_data.get("EVI", 0),
                    "savi": data.spectral_data.get("SAVI", 0),
                    "cloud_coverage": data.cloud_coverage,
                    "quality_score": data.quality_score
                })
            
            return {
                "vegetation_indices": indices_data,
                "total_records": len(indices_data),
                "location": {"lat": lat, "lon": lon},
                "date_range": {"start": start_date, "end": end_date}
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nasa/configuration")
async def get_nasa_configuration():
    """Get current NASA API configuration"""
    return {
        "api_key_configured": settings.nasa_api_key != "demo_key",
        "earth_data_url": settings.nasa_earth_data_url,
        "laads_daac_url": settings.nasa_laads_daac_url,
        "gibs_url": settings.nasa_gibs_url,
        "collections": {
            "landsat": settings.landsat_collection,
            "modis": settings.modis_collection,
            "viirs": settings.viirs_collection,
            "sentinel": settings.sentinel_collection
        },
        "spatial_resolution": settings.spatial_resolution,
        "cache_ttl": settings.cache_ttl
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
