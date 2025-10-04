# BloomTracker Data Directory

This directory contains sample geospatial datasets for the BloomTracker application.

## 📁 Dataset Structure

### MODIS Terra Vegetation Indices
- **Format**: HDF4-EOS
- **Content**: Vegetation indices (NDVI, EVI) and metadata
- **Note**: Large HDF files (>100MB) are excluded from repository due to GitHub size limits
- **Demo Data**: The application uses synthetic temporal data for predictions

### MERRA-2 Climate Data
- **Format**: NetCDF (.nc)
- **Content**: Climate variables and temporal data
- **Files**: LPRM-AMSR_E soil moisture data

### ALOS PALSAR Terrain Data
- **Format**: TIF, KMZ, XML, JPG, WLD
- **Content**: Radar backscatter, DEM, incidence maps
- **Note**: Some large TIF files (>50MB) are excluded from repository
- **Available**: Core radar data (HH, HV, VH, VV) and DEM files

## 🚀 Getting Started

The BloomTracker application is designed to work with or without the actual data files:

1. **With Data Files**: Full functionality with real geospatial processing
2. **Without Data Files**: Synthetic data generation for demonstration and testing

## 📊 Data Processing

The application includes intelligent fallback mechanisms:

- **MODIS**: Uses synthetic temporal data when HDF files are unavailable
- **MERRA-2**: Processes available NetCDF files for climate analysis
- **ALOS**: Handles available TIF files and generates summaries

## 🔧 Development

For development and testing, the application will:
- Generate realistic synthetic data
- Provide mock responses for API endpoints
- Maintain full functionality for demonstration purposes

## 📝 Notes

- Large files are excluded to comply with GitHub repository size limits
- The application is fully functional with synthetic data
- Real data files can be added locally for production use
- All API endpoints work regardless of data file availability
