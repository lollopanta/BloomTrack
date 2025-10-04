# BloomTrack Data Management Guide

## How to Change Data and Get Processing Results

### 🌐 **Accessing the System**

1. **Main Dashboard**: http://localhost:8000
2. **Data Management**: http://localhost:8000/data-management  
3. **Advanced Features**: http://localhost:8000/advanced
4. **API Documentation**: http://localhost:8000/api/docs

---

## 📊 **1. Adding New Bloom Data**

### Via Web Interface:
1. Go to **http://localhost:8000/data-management**
2. Fill in the "Input New Bloom Data" form:
   - **Location**: e.g., "California Central Valley"
   - **Region**: Select from dropdown
   - **Coordinates**: Latitude and Longitude
   - **Bloom Intensity**: Low/Medium/High
   - **Vegetation Type**: Agricultural/Forest/Grassland/etc.
   - **Confidence**: 0-100%
3. Click **"Add Bloom Event"**
4. See results in the processing results section

### Via API:
```bash
# Add new bloom event
curl -X POST "http://localhost:8000/api/bloom-events" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "New Location",
    "region": "North America",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "intensity": "high",
    "vegetation_type": "forest"
  }'
```

---

## 🔍 **2. Filtering and Querying Data**

### Via Web Interface:
1. Go to **Data Management** page
2. Select filter type:
   - **All Events**: Get all bloom events
   - **By Region**: Filter by geographic region
   - **By Intensity**: Filter by bloom intensity
   - **By Date Range**: Filter by time period
3. Click **"Apply Filters"**
4. View results in JSON format

### Via API:
```bash
# Get all bloom events
curl "http://localhost:8000/api/bloom-events"

# Filter by region
curl "http://localhost:8000/api/bloom-events?region=North%20America"

# Filter by intensity
curl "http://localhost:8000/api/bloom-events?intensity=high"

# Filter by date range
curl "http://localhost:8000/api/bloom-events?start_date=2024-01-01&end_date=2024-12-31"
```

---

## 🧠 **3. Running Data Processing**

### Spatial Analysis:
1. **Spatial Clustering**: Detects clusters of bloom events
   - Go to Data Management → Click "Spatial Analysis"
   - Results show cluster centers, event counts, and statistics

2. **Bloom Density**: Calculates spatial density
   - Shows density grid with intensity values
   - Identifies high-density bloom areas

3. **Temporal Patterns**: Analyzes seasonal trends
   - Shows yearly/monthly/seasonal counts
   - Identifies peak bloom periods
   - Calculates trend direction

### Machine Learning Predictions:
1. **Intensity Prediction**: Predict bloom intensity
   - Input: Location, date, vegetation type
   - Output: Predicted intensity (low/medium/high)
   - Confidence scores and probability distribution

2. **Timing Prediction**: Predict bloom timing
   - Input: Location, vegetation type
   - Output: Predicted bloom date and season

3. **Anomaly Detection**: Find unusual patterns
   - Identifies statistical outliers
   - Explains why events are anomalous

---

## 📈 **4. Getting Processing Results**

### Real-time Results:
- All processing happens in real-time
- Results appear immediately in the web interface
- JSON format for easy integration

### Result Types:

#### **Spatial Analysis Results:**
```json
{
  "clusters": [
    {
      "cluster_id": 0,
      "center_lat": 36.7783,
      "center_lon": -119.4179,
      "event_count": 3,
      "avg_intensity": 2.5,
      "total_area": 1500.5
    }
  ],
  "total_clusters": 2,
  "noise_points": 1
}
```

#### **ML Prediction Results:**
```json
{
  "predicted_intensity": "high",
  "confidence_score": 0.85,
  "probability_distribution": {
    "low": 0.1,
    "medium": 0.3,
    "high": 0.6
  }
}
```

#### **Temporal Analysis Results:**
```json
{
  "yearly_counts": {"2024": 15, "2023": 12},
  "monthly_counts": {"3": 5, "4": 8, "5": 2},
  "trend_direction": "increasing",
  "peak_months": [["4", 8], ["3", 5]]
}
```

---

## 🗺️ **5. Interactive Maps and Visualizations**

### Generate Maps:
1. Go to **Advanced Dashboard**
2. Click **"Load Interactive Map"**
3. View bloom events on satellite imagery
4. Hover over markers for details
5. Use heatmap overlay for intensity

### Conservation Priority Maps:
1. Click **"Load Priority Map"**
2. See color-coded priority levels:
   - **Red**: High priority (4-5)
   - **Orange**: Medium priority (3)
   - **Green**: Low priority (1-2)

---

## 💾 **6. Data Export**

### Export Formats:
1. **GeoJSON**: For GIS applications
2. **CSV**: For spreadsheet analysis
3. **KML**: For Google Earth

### Via Web Interface:
1. Go to **Data Management** page
2. Click export buttons (GeoJSON/CSV/KML)
3. File downloads automatically

### Via API:
```bash
# Export as GeoJSON
curl "http://localhost:8000/api/export/spatial-data?format=geojson"

# Export as CSV
curl "http://localhost:8000/api/export/spatial-data?format=csv"
```

---

## 🔧 **7. Advanced Processing**

### Training ML Models:
```bash
# Train intensity prediction model
curl -X POST "http://localhost:8000/api/ml/train-intensity-model"

# Train timing prediction model
curl -X POST "http://localhost:8000/api/ml/train-timing-model"
```

### Generate Forecasts:
```bash
# 6-month bloom forecast
curl "http://localhost:8000/api/ml/forecast?months=6"
```

### Analyze Anomalies:
```bash
# Detect anomalous bloom patterns
curl "http://localhost:8000/api/ml/analyze-anomalies"
```

---

## 📊 **8. Monitoring Results**

### Status Indicators:
- **🟢 Green**: Success
- **🔴 Red**: Error
- **🟠 Orange**: Processing

### Real-time Updates:
- All processing happens asynchronously
- Results update automatically
- No need to refresh the page

### Result History:
- All processing results are logged
- Timestamp for each result
- Easy to compare different analyses

---

## 🚀 **Quick Start Examples**

### Example 1: Add Data and Analyze
1. Go to `/data-management`
2. Add new bloom event
3. Run spatial analysis
4. Export results as CSV

### Example 2: Predict Bloom Timing
1. Go to `/advanced`
2. Train ML models
3. Input location and vegetation type
4. Get bloom timing prediction

### Example 3: Generate Conservation Map
1. Go to `/advanced`
2. Load conservation priority map
3. Identify high-priority areas
4. Export spatial data

---

## 🎯 **Best Practices**

1. **Start with Data Management** to understand your data
2. **Use Filters** to focus on specific regions/timeframes
3. **Run Multiple Analyses** to get comprehensive insights
4. **Export Results** for further analysis
5. **Monitor Status** to ensure processing completes
6. **Use API** for programmatic access

---

## 🔗 **API Endpoints Summary**

| Endpoint | Purpose | Method |
|----------|---------|---------|
| `/api/bloom-events` | Get/filter bloom events | GET |
| `/api/analysis/spatial-clusters` | Spatial clustering | GET |
| `/api/analysis/temporal-patterns` | Temporal analysis | GET |
| `/api/ml/predict-intensity` | ML intensity prediction | GET |
| `/api/ml/forecast` | Generate forecasts | GET |
| `/api/export/spatial-data` | Export data | GET |
| `/api/maps/interactive` | Generate maps | GET |

The BloomTrack system provides comprehensive data management and processing capabilities with real-time results and multiple export formats! 🌸🌍
