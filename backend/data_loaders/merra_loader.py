"""
MERRA-2 Data Loader for processing NetCDF files.

This module handles loading and processing of MERRA-2 climate data
stored in NetCDF format, extracting temporal and spatial variables.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import xarray as xr
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class MerraDataLoader:
    """
    Data loader for MERRA-2 climate data NetCDF files.
    
    This class handles the processing of MERRA-2 NetCDF files to extract
    climate variables, temporal data, and spatial information.
    """
    
    def __init__(self, data_path: str = "Data/MERRA-2 const_2d_lnd_Nx"):
        """
        Initialize the MERRA-2 data loader.
        
        Args:
            data_path (str): Path to the MERRA-2 data directory
        """
        self.data_path = Path(data_path)
        self.description_file = self.data_path / "description.json"
        
    def load_data(self) -> Dict[str, Any]:
        """
        Load and process all MERRA-2 NetCDF files in the data directory.
        
        Returns:
            Dict containing processed MERRA-2 data with climate variables and metadata
        """
        try:
            logger.info(f"Loading MERRA-2 data from {self.data_path}")
            
            # Load description
            description = self._load_description()
            
            # Find and process NetCDF files
            nc_files = list(self.data_path.glob("*.nc"))
            processed_files = []
            
            for nc_file in nc_files:
                try:
                    file_data = self._process_netcdf_file(nc_file)
                    processed_files.append(file_data)
                    logger.info(f"Successfully processed {nc_file.name}")
                except Exception as e:
                    logger.error(f"Error processing {nc_file.name}: {str(e)}")
                    continue
            
            return {
                "description": description,
                "files": processed_files,
                "total_files": len(processed_files),
                "data_type": "MERRA-2 const_2d_lnd_Nx"
            }
            
        except Exception as e:
            logger.error(f"Error loading MERRA-2 data: {str(e)}")
            raise
    
    def _load_description(self) -> Dict[str, Any]:
        """
        Load the description.json file for MERRA-2 data.
        
        Returns:
            Dict containing the description information
        """
        try:
            if self.description_file.exists():
                with open(self.description_file, 'r') as f:
                    return json.load(f)
            else:
                return {"description": "MERRA-2 const_2d_lnd_Nx data"}
        except Exception as e:
            logger.warning(f"Could not load description file: {str(e)}")
            return {"description": "MERRA-2 const_2d_lnd_Nx data"}
    
    def _process_netcdf_file(self, nc_file: Path) -> Dict[str, Any]:
        """
        Process a single NetCDF file to extract climate variables and metadata.
        
        Args:
            nc_file (Path): Path to the NetCDF file
            
        Returns:
            Dict containing processed data from the NetCDF file
        """
        try:
            with xr.open_dataset(nc_file) as ds:
                # Extract file metadata
                file_info = {
                    "filename": nc_file.name,
                    "file_size": nc_file.stat().st_size,
                    "dimensions": dict(ds.dims),
                    "coordinates": list(ds.coords.keys()),
                    "data_vars": list(ds.data_vars.keys()),
                    "attributes": dict(ds.attrs)
                }
                
                # Process climate variables
                climate_data = self._extract_climate_variables(ds)
                
                # Process temporal information
                temporal_data = self._extract_temporal_info(ds)
                
                # Process spatial information
                spatial_data = self._extract_spatial_info(ds)
                
                return {
                    "file_info": file_info,
                    "climate_variables": climate_data,
                    "temporal_info": temporal_data,
                    "spatial_info": spatial_data
                }
                
        except Exception as e:
            logger.error(f"Error processing NetCDF file {nc_file.name}: {str(e)}")
            raise
    
    def _extract_climate_variables(self, dataset: xr.Dataset) -> Dict[str, Any]:
        """
        Extract climate variables from the NetCDF dataset.
        
        Args:
            dataset: xarray Dataset object
            
        Returns:
            Dict containing climate variable statistics
        """
        climate_data = {}
        
        for var_name, var_data in dataset.data_vars.items():
            try:
                # Get data array
                data = var_data.values
                
                # Calculate statistics (excluding NaN values)
                valid_data = data[~np.isnan(data)]
                
                if len(valid_data) > 0:
                    climate_data[var_name] = {
                        "shape": var_data.shape,
                        "dtype": str(var_data.dtype),
                        "dimensions": list(var_data.dims),
                        "min_value": float(np.min(valid_data)),
                        "max_value": float(np.max(valid_data)),
                        "mean_value": float(np.mean(valid_data)),
                        "std_value": float(np.std(valid_data)),
                        "valid_values": len(valid_data),
                        "total_values": data.size,
                        "attributes": dict(var_data.attrs),
                        "units": var_data.attrs.get('units', 'unknown')
                    }
                    
                    # Add coordinate information if available
                    if hasattr(var_data, 'coords'):
                        climate_data[var_name]["coordinates"] = {
                            coord: {
                                "values": coord_data.values.tolist() if len(coord_data.values) < 100 else "large_array",
                                "attributes": dict(coord_data.attrs)
                            } for coord, coord_data in var_data.coords.items()
                        }
                        
            except Exception as e:
                logger.warning(f"Error processing variable {var_name}: {str(e)}")
                continue
        
        return climate_data
    
    def _extract_temporal_info(self, dataset: xr.Dataset) -> Dict[str, Any]:
        """
        Extract temporal information from the dataset.
        
        Args:
            dataset: xarray Dataset object
            
        Returns:
            Dict containing temporal information
        """
        temporal_data = {}
        
        # Look for time-related coordinates
        time_coords = ['time', 'Time', 'TIME']
        
        for time_coord in time_coords:
            if time_coord in dataset.coords:
                time_data = dataset[time_coord]
                try:
                    temporal_data[time_coord] = {
                        "values": time_data.values.tolist() if len(time_data.values) < 100 else "large_array",
                        "dtype": str(time_data.dtype),
                        "attributes": dict(time_data.attrs),
                        "min_value": str(time_data.min().values) if hasattr(time_data, 'min') else None,
                        "max_value": str(time_data.max().values) if hasattr(time_data, 'max') else None
                    }
                except Exception as e:
                    logger.warning(f"Error processing time coordinate {time_coord}: {str(e)}")
                    continue
        
        return temporal_data
    
    def _extract_spatial_info(self, dataset: xr.Dataset) -> Dict[str, Any]:
        """
        Extract spatial information from the dataset.
        
        Args:
            dataset: xarray Dataset object
            
        Returns:
            Dict containing spatial information
        """
        spatial_data = {}
        
        # Look for spatial coordinates
        spatial_coords = ['lat', 'lon', 'latitude', 'longitude', 'x', 'y']
        
        for spatial_coord in spatial_coords:
            if spatial_coord in dataset.coords:
                coord_data = dataset[spatial_coord]
                try:
                    spatial_data[spatial_coord] = {
                        "values": coord_data.values.tolist() if len(coord_data.values) < 100 else "large_array",
                        "dtype": str(coord_data.dtype),
                        "attributes": dict(coord_data.attrs),
                        "min_value": float(coord_data.min().values) if hasattr(coord_data, 'min') else None,
                        "max_value": float(coord_data.max().values) if hasattr(coord_data, 'max') else None,
                        "shape": coord_data.shape
                    }
                except Exception as e:
                    logger.warning(f"Error processing spatial coordinate {spatial_coord}: {str(e)}")
                    continue
        
        return spatial_data
