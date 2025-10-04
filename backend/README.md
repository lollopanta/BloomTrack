# BloomTracker Backend

A FastAPI-based backend service for processing and serving geospatial data from multiple satellite and climate data sources.

## 🌍 Overview

BloomTracker is designed to process heterogeneous geospatial datasets and convert them into structured, machine-readable JSON/GeoJSON format. The backend handles three main data sources:

- **MODIS Terra Vegetation Indices** (.hdf files) - Vegetation monitoring data
- **MERRA-2 Climate Data** (.nc files) - Atmospheric reanalysis data
- **ALOS PALSAR Terrain Data** (.tif, .kmz, .xml files) - Synthetic Aperture Radar data

## 🏗️ Project Structure

```
BloomTracker/
└── backend/
    ├── main.py                    # FastAPI application entry point
    ├── requirements.txt           # Python dependencies
    ├── README.md                  # This documentation
    ├── logs/                      # Application logs directory
    ├── data_loaders/              # Data processing modules
    │   ├── __init__.py
    │   ├── modis_loader.py        # MODIS HDF file processor
    │   ├── merra_loader.py        # MERRA-2 NetCDF file processor
    │   └── alos_loader.py         # ALOS PALSAR terrain data processor
    └── Data/                      # Geospatial data directory
        ├── MODIS Terra Vegetation Indices/
        ├── MERRA-2 const_2d_lnd_Nx/
        └── ALOS PALSAR High Resolution Radiometric Terrain/
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**

   ```bash
   cd backend
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## 📊 API Endpoints

### Core Endpoints

| Endpoint          | Method | Description                             |
| ----------------- | ------ | --------------------------------------- |
| `/`               | GET    | API information and available endpoints |
| `/health`         | GET    | Health check endpoint                   |
| `/data/modis`     | GET    | Process MODIS vegetation indices data   |
| `/data/merra`     | GET    | Process MERRA-2 climate data            |
| `/data/alos`      | GET    | Process ALOS PALSAR terrain data        |
| `/data/all`       | GET    | Process all available data sources      |
| `/predict/modis`  | GET    | Predict vegetation index trends         |
| `/predict/merra`  | GET    | Predict climate variables               |
| `/predict/alos`   | GET    | Predict terrain changes                 |
| `/predict/all`    | GET    | Multi-source predictions                |
| `/predict/train`  | POST   | Train and save models                   |
| `/predict/models` | GET    | List saved models                       |

### Response Format

All data endpoints return responses in the following format:

```json
{
  "success": true,
  "data": {
    "description": "...",
    "files": [...],
    "total_files": 3,
    "data_type": "..."
  },
  "metadata": {
    "source": "...",
    "file_type": "...",
    "processed_files": 3
  },
  "message": "Data processed successfully"
}
```

## 🔮 Prediction API

BloomTracker now includes a predictive analytics system that forecasts future geospatial and environmental trends using time-series data from MODIS, MERRA-2, and ALOS PALSAR datasets.

### Prediction Endpoints

| Endpoint          | Method | Description                                                                                       |
| ----------------- | ------ | ------------------------------------------------------------------------------------------------- |
| `/predict/modis`  | GET    | Predicts vegetation index trends (NDVI, EVI) from MODIS HDF data                                  |
| `/predict/merra`  | GET    | Predicts future climate variables (temperature, humidity, soil moisture) from MERRA-2 NetCDF data |
| `/predict/alos`   | GET    | Estimates terrain reflectivity or surface changes from ALOS PALSAR time-ordered data              |
| `/predict/all`    | GET    | Combines all datasets for a unified multi-source forecast                                         |
| `/predict/train`  | POST   | Forces model retraining and saves updated versions                                                |
| `/predict/models` | GET    | Lists all saved models with metadata                                                              |

### Model Types

The prediction system supports three machine learning models with automatic selection:

- **ARIMA**: AutoRegressive Integrated Moving Average for stationary time series
- **Prophet**: Facebook's Prophet for seasonal and trend-based forecasting
- **LSTM**: Long Short-Term Memory neural networks for complex patterns

### Example Prediction Requests

```bash
# Predict MODIS vegetation trends
curl -X GET "http://localhost:8000/predict/modis?model=prophet&steps=10"

# Predict MERRA-2 climate variables
curl -X GET "http://localhost:8000/predict/merra?model=lstm&steps=7"

# Multi-source prediction
curl -X GET "http://localhost:8000/predict/all?model=auto&steps=5"

# Train new model
curl -X POST "http://localhost:8000/predict/train?dataset=merra&model=prophet"
```

### Example Prediction Response

```json
{
  "success": true,
  "data": {
    "predicted_values": [292.1, 292.3, 292.7, 292.9, 293.0],
    "timestamps": [
      "2025-10-05",
      "2025-10-06",
      "2025-10-07",
      "2025-10-08",
      "2025-10-09"
    ],
    "model_used": "Prophet",
    "source": "MERRA-2 Climate Data"
  },
  "metadata": {
    "processed_files": 3,
    "confidence": 0.91,
    "training_samples": 40
  },
  "message": "5-step forecast generated successfully using Prophet model."
}
```

### How Models Work

- **MODIS Predictions**: Analyzes NDVI/EVI time series to forecast vegetation health and growth patterns
- **MERRA-2 Predictions**: Uses climate variables to predict temperature, humidity, and atmospheric conditions
- **ALOS PALSAR Predictions**: Processes radar data to forecast surface changes and terrain reflectivity
- **Multi-Source**: Combines all data sources for comprehensive environmental forecasting

### Model Management

- Models are automatically saved and loaded from `models/saved_models/`
- Automatic model selection based on data characteristics and sample size
- Model freshness checking with configurable retraining intervals
- Persistent storage with metadata tracking

## 🔧 Data Processing Details

### MODIS Terra Vegetation Indices (.hdf files)

**Library Used:** `h5py` for HDF5 file reading

**Data Extracted:**

- NDVI (Normalized Difference Vegetation Index)
- EVI (Enhanced Vegetation Index)
- Reflectance bands (Red, NIR, Blue, MIR)
- Quality assurance layers
- Spatial and temporal metadata

**Processing Features:**

- Statistical analysis of vegetation indices
- Quality layer interpretation
- Band-specific statistics
- Fill value handling

### MERRA-2 Climate Data (.nc files)

**Library Used:** `xarray` and `netCDF4` for NetCDF file processing

**Data Extracted:**

- Climate variables (temperature, humidity, pressure, etc.)
- Temporal information (time series data)
- Spatial coordinates (latitude, longitude)
- Variable attributes and units

**Processing Features:**

- Multi-dimensional data handling
- Coordinate system extraction
- Temporal analysis
- Variable statistics

### ALOS PALSAR Terrain Data (Multiple formats)

**Libraries Used:**

- `rasterio` for TIF files
- `zipfile` for KMZ files
- `xml.etree.ElementTree` for XML files
- `PIL` for image files

**File Types Processed:**

- **TIF files:** Geospatial raster data with coordinate information
- **KMZ files:** Compressed KML files with embedded imagery
- **XML files:** Metadata and configuration files
- **JPG files:** Georeferenced imagery
- **WLD files:** World files for georeferencing

**Processing Features:**

- Bounding box extraction
- Coordinate system detection
- Band statistics for raster data
- Metadata extraction from various formats

## 🛠️ Technical Architecture

### Data Loading Strategy

The backend uses a modular approach with specialized data loaders:

1. **File Type Detection:** Automatic detection of file types and selection of appropriate parser
2. **Error Handling:** Graceful handling of missing files and unsupported formats
3. **Logging:** Comprehensive logging of all operations to `logs/app.log`
4. **Extensibility:** Easy addition of new data sources through the loader pattern

### Prediction System Architecture

The prediction system consists of three main components:

1. **PredictiveModel Class**: Core forecasting engine supporting ARIMA, Prophet, and LSTM models
2. **TimeSeriesPredictor**: Integrates with data loaders to extract time-series data for forecasting
3. **ModelManager**: Handles persistent storage, loading, and management of trained models

### Machine Learning Pipeline

1. **Data Extraction**: Time-series data extracted from geospatial datasets
2. **Model Selection**: Automatic selection based on data characteristics (seasonality, stationarity, sample size)
3. **Training**: Models trained on historical data with validation
4. **Prediction**: Future forecasts generated with confidence intervals
5. **Persistence**: Trained models saved for future use with metadata tracking

### Key Libraries and Their Purposes

| Library     | Purpose                      | File Types           |
| ----------- | ---------------------------- | -------------------- |
| `h5py`      | HDF5 file reading            | .hdf files           |
| `xarray`    | NetCDF data processing       | .nc files            |
| `rasterio`  | Geospatial raster data       | .tif files           |
| `geopandas` | Geospatial data manipulation | Vector data          |
| `shapely`   | Geometric operations         | Spatial calculations |
| `zipfile`   | Archive file handling        | .kmz files           |
| `fastapi`   | Web framework                | API endpoints        |
| `uvicorn`   | ASGI server                  | Application server   |

## 📝 Example API Requests

### Get MODIS Data

```bash
curl -X GET "http://localhost:8000/data/modis"
```

### Get MERRA-2 Data

```bash
curl -X GET "http://localhost:8000/data/merra"
```

### Get ALOS PALSAR Data

```bash
curl -X GET "http://localhost:8000/data/alos"
```

### Get All Data

```bash
curl -X GET "http://localhost:8000/data/all"
```

## 📋 Example Response

```json
{
  "success": true,
  "data": {
    "description": "MODIS Terra Vegetation Indices data",
    "files": [
      {
        "file_info": {
          "filename": "MOD13Q1.A2025257.h12v10.061.2025275114431.hdf",
          "file_size": 1234567,
          "datasets": ["NDVI", "EVI", "Quality"],
          "attributes": {...}
        },
        "vegetation_indices": {
          "NDVI": {
            "shape": [2400, 2400],
            "min_value": -0.2,
            "max_value": 0.9,
            "mean_value": 0.45,
            "valid_pixels": 5760000
          }
        }
      }
    ],
    "total_files": 1,
    "data_type": "MODIS Terra Vegetation Indices"
  },
  "metadata": {
    "source": "MODIS Terra Vegetation Indices",
    "file_type": "HDF",
    "processed_files": 1
  },
  "message": "MODIS data processed successfully"
}
```

## 🔍 Logging

The application logs all operations to `logs/app.log` with the following information:

- Data processing status
- Error messages and stack traces
- File processing results
- API request/response information

## 🚨 Error Handling

The backend includes comprehensive error handling for:

- Missing data files
- Unsupported file formats
- Corrupted data files
- Network connectivity issues
- Memory limitations

All errors are logged and returned as appropriate HTTP status codes with descriptive error messages.

## 🔧 Configuration

The application can be configured by modifying the data paths in each loader class:

```python
# In modis_loader.py
self.data_path = Path("Data/MODIS Terra Vegetation Indices")

# In merra_loader.py
self.data_path = Path("Data/MERRA-2 const_2d_lnd_Nx")

# In alos_loader.py
self.data_path = Path("Data/ALOS PALSAR High Resolution Radiometric Terrain")
```

## 🚀 Deployment

For production deployment, consider:

1. **Environment Variables:** Use environment variables for configuration
2. **Database Integration:** Add database support for data caching
3. **Authentication:** Implement API authentication if needed
4. **Caching:** Add Redis or similar for response caching
5. **Load Balancing:** Use multiple worker processes with Gunicorn

## 🤝 Contributing

To extend the backend with new data sources:

1. Create a new loader class in `data_loaders/`
2. Implement the `load_data()` method
3. Add the new endpoint to `main.py`
4. Update this documentation

## 📄 License

This project is part of the BloomTracker system for geospatial data processing and analysis.
