"""
BloomTracker Backend - FastAPI application for processing geospatial data

This module provides REST API endpoints to process and serve data from:
- MODIS Terra Vegetation Indices (.hdf files)
- MERRA-2 climate data (.nc files) 
- ALOS PALSAR terrain data (.tif, .kmz, .xml files)

Author: BloomTracker Team
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our custom data loaders
from data_loaders.modis_loader import ModisDataLoader
from data_loaders.merra_loader import MerraDataLoader
from data_loaders.alos_loader import AlosDataLoader

# Import prediction router
from prediction.router import router as prediction_router

# Import plant analysis router
from plant_analysis.plant_router import router as plant_router
from plant_analysis.plant_ai_router import router as plant_ai_router

# Configure logging
def setup_logging():
    """Set up logging configuration for the application."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BloomTracker API",
    description="REST API for processing and serving geospatial data from MODIS, MERRA-2, and ALOS PALSAR datasets",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Setup logging
logger = setup_logging()

# Initialize data loaders
modis_loader = ModisDataLoader()
merra_loader = MerraDataLoader()
alos_loader = AlosDataLoader()

# Include prediction router
app.include_router(prediction_router)

# Include plant analysis router
app.include_router(plant_router)
app.include_router(plant_ai_router)

# Pydantic models for API responses
class DataResponse(BaseModel):
    """Base response model for data endpoints."""
    success: bool
    data: Any
    metadata: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    details: Optional[str] = None

@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        Dict containing API information and available endpoints
    """
    return {
        "message": "BloomTracker API",
        "version": "1.0.0",
        "endpoints": {
            "modis": "/data/modis",
            "merra": "/data/merra", 
            "alos": "/data/alos",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status.
    
    Returns:
        Dict containing health status
    """
    return {"status": "healthy", "service": "BloomTracker API"}

@app.get("/data/modis", response_model=DataResponse)
async def get_modis_data():
    """
    Retrieve and process MODIS Terra Vegetation Indices data.
    
    Processes .hdf files from the MODIS Terra Vegetation Indices folder,
    extracting vegetation indices (NDVI, EVI) and metadata.
    
    Returns:
        DataResponse containing processed MODIS data
    """
    try:
        logger.info("Processing MODIS data request")
        data = modis_loader.load_data()
        
        return DataResponse(
            success=True,
            data=data,
            metadata={
                "source": "MODIS Terra Vegetation Indices",
                "file_type": "HDF",
                "processed_files": len(data.get("files", []))
            },
            message="MODIS data processed successfully"
        )
    except Exception as e:
        logger.error(f"Error processing MODIS data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing MODIS data: {str(e)}")

@app.get("/data/merra", response_model=DataResponse)
async def get_merra_data():
    """
    Retrieve and process MERRA-2 climate data.
    
    Processes .nc (NetCDF) files from the MERRA-2 folder,
    extracting temporal and spatial climate variables.
    
    Returns:
        DataResponse containing processed MERRA-2 data
    """
    try:
        logger.info("Processing MERRA-2 data request")
        data = merra_loader.load_data()
        
        return DataResponse(
            success=True,
            data=data,
            metadata={
                "source": "MERRA-2 const_2d_lnd_Nx",
                "file_type": "NetCDF",
                "processed_files": len(data.get("files", []))
            },
            message="MERRA-2 data processed successfully"
        )
    except Exception as e:
        logger.error(f"Error processing MERRA-2 data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing MERRA-2 data: {str(e)}")

@app.get("/data/alos", response_model=DataResponse)
async def get_alos_data():
    """
    Retrieve and process ALOS PALSAR terrain data.
    
    Processes .tif, .kmz, .xml, .jpg, and .wld files from the ALOS PALSAR folder,
    extracting geospatial information and creating summaries.
    
    Returns:
        DataResponse containing processed ALOS PALSAR data
    """
    try:
        logger.info("Processing ALOS PALSAR data request")
        data = alos_loader.load_data()
        
        return DataResponse(
            success=True,
            data=data,
            metadata={
                "source": "ALOS PALSAR High Resolution Radiometric Terrain",
                "file_types": ["TIF", "KMZ", "XML", "JPG", "WLD"],
                "processed_files": len(data.get("files", []))
            },
            message="ALOS PALSAR data processed successfully"
        )
    except Exception as e:
        logger.error(f"Error processing ALOS PALSAR data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing ALOS PALSAR data: {str(e)}")

@app.get("/data/all", response_model=DataResponse)
async def get_all_data():
    """
    Retrieve and process all available data sources.
    
    Combines data from MODIS, MERRA-2, and ALOS PALSAR sources.
    
    Returns:
        DataResponse containing all processed data
    """
    try:
        logger.info("Processing all data sources request")
        
        all_data = {
            "modis": modis_loader.load_data(),
            "merra": merra_loader.load_data(),
            "alos": alos_loader.load_data()
        }
        
        return DataResponse(
            success=True,
            data=all_data,
            metadata={
                "sources": ["MODIS", "MERRA-2", "ALOS PALSAR"],
                "total_files": sum(len(data.get("files", [])) for data in all_data.values())
            },
            message="All data sources processed successfully"
        )
    except Exception as e:
        logger.error(f"Error processing all data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing all data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
