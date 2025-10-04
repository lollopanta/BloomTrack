# BloomTrack - Plant Blooming Event Monitoring System

A comprehensive Python application for monitoring and visualizing plant blooming events using NASA Earth observation data. Built with FastAPI, GeoPandas, and modern web technologies.

## 🌸 Features

- **Global Bloom Monitoring**: Track plant blooming events across the globe
- **NASA Data Integration**: Leverage satellite data from Landsat, MODIS, VIIRS, and other missions
- **Interactive Dashboard**: Beautiful web interface with Bulma CSS
- **Geospatial Analysis**: Advanced spatial data processing with GeoPandas
- **Real-time Detection**: AI-powered bloom event detection
- **Conservation Insights**: Priority areas and ecological impact analysis
- **Temporal Analysis**: Track bloom patterns over time
- **API-First Design**: RESTful API for data access and integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BloomTrack
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs
   - Alternative API Docs: http://localhost:8000/api/redoc

## 📊 API Endpoints

### Core Endpoints

- `GET /` - Main dashboard with interactive bloom cards
- `GET /api/bloom-events` - Get plant blooming events with filtering
- `GET /api/satellite-data` - Get satellite data for specific coordinates
- `GET /api/bloom-detection` - Detect bloom events in an area
- `GET /api/visualization/heatmap` - Generate bloom intensity heatmaps
- `GET /api/statistics/global` - Get global bloom statistics
- `GET /api/health` - Health check endpoint

### Query Parameters

#### Bloom Events Filtering
- `region`: Filter by geographic region
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `intensity`: Filter by bloom intensity (high/medium/low)

#### Satellite Data
- `lat`: Latitude coordinate
- `lon`: Longitude coordinate
- `start_date`: Start date for data range
- `end_date`: End date for data range

#### Bloom Detection
- `lat`: Search latitude
- `lon`: Search longitude
- `radius`: Search radius in kilometers (default: 10.0)

## 🛠️ Architecture

### Backend Components

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and serialization
- **GeoPandas**: Geospatial data processing
- **Matplotlib**: Data visualization
- **NumPy/Pandas**: Data manipulation and analysis

### Data Models

- `PlantBloomEvent`: Core bloom event data
- `SatelliteData`: Satellite observation data
- `BloomDetection`: Detection results and analysis
- `GlobalStatistics`: Aggregated statistics
- `HeatmapData`: Visualization data

### Services

- `DataProcessor`: Core data processing and analysis
- `NASADataService`: NASA API integration
- `VisualizationService`: Chart and map generation

## 🌍 Supported Data Sources

- **Landsat**: High-resolution multispectral imagery
- **MODIS**: Moderate resolution daily observations
- **VIIRS**: Visible Infrared Imaging Radiometer Suite
- **Sentinel**: European Space Agency satellites
- **PACE**: Plankton, Aerosol, Cloud, ocean Ecosystem
- **EMIT**: Earth Surface Mineral Dust Source Investigation

## 📈 Use Cases

### Agricultural Monitoring
- Crop flowering detection
- Harvest timing optimization
- Pest and disease management
- Yield prediction

### Conservation Biology
- Pollinator habitat assessment
- Invasive species detection
- Ecosystem health monitoring
- Biodiversity tracking

### Climate Research
- Phenology studies
- Climate change impact assessment
- Seasonal pattern analysis
- Anomaly detection

### Public Health
- Pollen forecasting
- Allergy management
- Air quality monitoring
- Disease vector tracking

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
NASA_API_KEY=your_nasa_api_key
DATABASE_URL=postgresql://user:password@localhost/bloomtrack
REDIS_URL=redis://localhost:6379
DEBUG=True
```

### Database Setup

The application can be configured to use PostgreSQL for persistent data storage:

```bash
# Install PostgreSQL dependencies
pip install psycopg2-binary sqlalchemy alembic

# Run migrations
alembic upgrade head
```

## 📊 Sample Data

The application includes sample bloom events from various global locations:

- **California Central Valley**: Agricultural bloom events
- **Amazon Rainforest**: Tropical forest blooms
- **Sahara Desert**: Rare desert bloom events
- **Australian Outback**: Post-fire recovery blooms
- **Siberian Tundra**: Arctic bloom events

## 🎨 Frontend Features

- **Responsive Design**: Mobile-friendly interface
- **Interactive Cards**: Beautiful bloom event cards with Bulma CSS
- **Real-time Loading**: Dynamic data loading with JavaScript
- **Color-coded Indicators**: Visual intensity indicators
- **Filtering Options**: Advanced filtering capabilities

## 🔬 Scientific Applications

### Vegetation Indices
- **NDVI**: Normalized Difference Vegetation Index
- **EVI**: Enhanced Vegetation Index
- **SAVI**: Soil Adjusted Vegetation Index

### Analysis Methods
- Temporal trend analysis
- Anomaly detection
- Spatial clustering
- Conservation priority mapping

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NASA Earth Observation Data
- USGS Landsat Program
- European Space Agency Sentinel Program
- Open source geospatial libraries

## 📞 Support

For questions, issues, or contributions, please:

1. Check the API documentation at `/api/docs`
2. Review the sample data and endpoints
3. Open an issue on GitHub
4. Contact the development team

---

**BloomTrack** - Monitoring the pulse of life across our planet! 🌍🌸
