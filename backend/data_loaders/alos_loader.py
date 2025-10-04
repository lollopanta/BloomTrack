"""
ALOS PALSAR Data Loader for processing terrain data files.

This module handles loading and processing of ALOS PALSAR terrain data
including TIF, KMZ, XML, JPG, and WLD files to extract geospatial information.
"""

import os
import json
import logging
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional
import rasterio
from rasterio.crs import CRS
import geopandas as gpd
from shapely.geometry import box
import xml.etree.ElementTree as ET
from PIL import Image

logger = logging.getLogger(__name__)

class AlosDataLoader:
    """
    Data loader for ALOS PALSAR terrain data files.
    
    This class handles the processing of various ALOS PALSAR file formats
    including TIF, KMZ, XML, JPG, and WLD files to extract geospatial information.
    """
    
    def __init__(self, data_path: str = "Data/ALOS PALSAR High Resolution Radiometric Terrain"):
        """
        Initialize the ALOS PALSAR data loader.
        
        Args:
            data_path (str): Path to the ALOS PALSAR data directory
        """
        self.data_path = Path(data_path)
        self.description_file = self.data_path / "description.json"
        
    def load_data(self) -> Dict[str, Any]:
        """
        Load and process all ALOS PALSAR files in the data directory.
        
        Returns:
            Dict containing processed ALOS PALSAR data with geospatial information
        """
        try:
            logger.info(f"Loading ALOS PALSAR data from {self.data_path}")
            
            # Load description
            description = self._load_description()
            
            # Process different file types
            processed_data = {
                "tif_files": self._process_tif_files(),
                "kmz_files": self._process_kmz_files(),
                "xml_files": self._process_xml_files(),
                "image_files": self._process_image_files(),
                "geo_files": self._process_geo_files()
            }
            
            # Calculate summary statistics
            total_files = sum(len(files) for files in processed_data.values())
            
            return {
                "description": description,
                "file_types": processed_data,
                "total_files": total_files,
                "data_type": "ALOS PALSAR High Resolution Radiometric Terrain"
            }
            
        except Exception as e:
            logger.error(f"Error loading ALOS PALSAR data: {str(e)}")
            raise
    
    def _load_description(self) -> Dict[str, Any]:
        """
        Load the description.json file for ALOS PALSAR data.
        
        Returns:
            Dict containing the description information
        """
        try:
            if self.description_file.exists():
                with open(self.description_file, 'r') as f:
                    return json.load(f)
            else:
                return {"description": "ALOS PALSAR High Resolution Radiometric Terrain data"}
        except Exception as e:
            logger.warning(f"Could not load description file: {str(e)}")
            return {"description": "ALOS PALSAR High Resolution Radiometric Terrain data"}
    
    def _process_tif_files(self) -> List[Dict[str, Any]]:
        """
        Process TIF files to extract geospatial information.
        
        Returns:
            List of processed TIF file information
        """
        tif_files = []
        tif_dir = self.data_path / "tif"
        
        if not tif_dir.exists():
            logger.warning("TIF directory not found")
            return tif_files
        
        for tif_file in tif_dir.glob("*.tif"):
            try:
                with rasterio.open(tif_file) as src:
                    # Extract geospatial information
                    file_info = {
                        "filename": tif_file.name,
                        "file_size": tif_file.stat().st_size,
                        "driver": src.driver,
                        "width": src.width,
                        "height": src.height,
                        "count": src.count,
                        "dtype": str(src.dtypes[0]),
                        "crs": str(src.crs) if src.crs else None,
                        "transform": src.transform.to_gdal(),
                        "bounds": src.bounds,
                        "nodata": src.nodata,
                        "attributes": dict(src.tags())
                    }
                    
                    # Calculate bounding box
                    bounds = src.bounds
                    bbox = {
                        "minx": bounds.left,
                        "miny": bounds.bottom,
                        "maxx": bounds.right,
                        "maxy": bounds.top
                    }
                    file_info["bounding_box"] = bbox
                    
                    # Extract band information
                    bands_info = []
                    for i in range(1, src.count + 1):
                        band = src.read(i)
                        bands_info.append({
                            "band": i,
                            "shape": band.shape,
                            "dtype": str(band.dtype),
                            "min_value": float(band.min()),
                            "max_value": float(band.max()),
                            "mean_value": float(band.mean()),
                            "std_value": float(band.std())
                        })
                    file_info["bands"] = bands_info
                    
                    tif_files.append(file_info)
                    logger.info(f"Successfully processed TIF file: {tif_file.name}")
                    
            except Exception as e:
                logger.error(f"Error processing TIF file {tif_file.name}: {str(e)}")
                continue
        
        return tif_files
    
    def _process_kmz_files(self) -> List[Dict[str, Any]]:
        """
        Process KMZ files to extract geospatial information.
        
        Returns:
            List of processed KMZ file information
        """
        kmz_files = []
        kmz_dir = self.data_path / "kmz"
        
        if not kmz_dir.exists():
            logger.warning("KMZ directory not found")
            return kmz_files
        
        for kmz_file in kmz_dir.glob("*.kmz"):
            try:
                file_info = {
                    "filename": kmz_file.name,
                    "file_size": kmz_file.stat().st_size,
                    "file_type": "KMZ"
                }
                
                # Extract KMZ contents
                with zipfile.ZipFile(kmz_file, 'r') as kmz:
                    file_list = kmz.namelist()
                    file_info["contents"] = file_list
                    
                    # Look for KML files
                    kml_files = [f for f in file_list if f.endswith('.kml')]
                    if kml_files:
                        # Read the first KML file
                        kml_content = kmz.read(kml_files[0]).decode('utf-8')
                        file_info["kml_content"] = kml_content[:1000]  # First 1000 chars
                    
                    # Look for image files
                    image_files = [f for f in file_list if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                    file_info["image_files"] = image_files
                
                kmz_files.append(file_info)
                logger.info(f"Successfully processed KMZ file: {kmz_file.name}")
                
            except Exception as e:
                logger.error(f"Error processing KMZ file {kmz_file.name}: {str(e)}")
                continue
        
        return kmz_files
    
    def _process_xml_files(self) -> List[Dict[str, Any]]:
        """
        Process XML files to extract metadata.
        
        Returns:
            List of processed XML file information
        """
        xml_files = []
        xml_dir = self.data_path / "xml"
        
        if not xml_dir.exists():
            logger.warning("XML directory not found")
            return xml_files
        
        for xml_file in xml_dir.glob("*.xml"):
            try:
                file_info = {
                    "filename": xml_file.name,
                    "file_size": xml_file.stat().st_size,
                    "file_type": "XML"
                }
                
                # Parse XML content
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Extract basic XML structure
                file_info["root_tag"] = root.tag
                file_info["root_attributes"] = dict(root.attrib)
                file_info["child_elements"] = [child.tag for child in root]
                
                # Extract specific metadata if available
                metadata = {}
                for elem in root.iter():
                    if elem.text and elem.text.strip():
                        metadata[elem.tag] = elem.text.strip()
                
                file_info["metadata"] = metadata
                xml_files.append(file_info)
                logger.info(f"Successfully processed XML file: {xml_file.name}")
                
            except Exception as e:
                logger.error(f"Error processing XML file {xml_file.name}: {str(e)}")
                continue
        
        return xml_files
    
    def _process_image_files(self) -> List[Dict[str, Any]]:
        """
        Process image files (JPG) to extract basic information.
        
        Returns:
            List of processed image file information
        """
        image_files = []
        image_dir = self.data_path / "image"
        
        if not image_dir.exists():
            logger.warning("Image directory not found")
            return image_files
        
        for image_file in image_dir.glob("*.jpg"):
            try:
                with Image.open(image_file) as img:
                    file_info = {
                        "filename": image_file.name,
                        "file_size": image_file.stat().st_size,
                        "file_type": "JPG",
                        "width": img.width,
                        "height": img.height,
                        "mode": img.mode,
                        "format": img.format,
                        "has_transparency": img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                    }
                    
                    # Extract EXIF data if available
                    if hasattr(img, '_getexif') and img._getexif():
                        file_info["exif_data"] = "Available"
                    
                    image_files.append(file_info)
                    logger.info(f"Successfully processed image file: {image_file.name}")
                    
            except Exception as e:
                logger.error(f"Error processing image file {image_file.name}: {str(e)}")
                continue
        
        return image_files
    
    def _process_geo_files(self) -> List[Dict[str, Any]]:
        """
        Process GEO files (world files) to extract geospatial information.
        
        Returns:
            List of processed GEO file information
        """
        geo_files = []
        geo_dir = self.data_path / "geo"
        
        if not geo_dir.exists():
            logger.warning("GEO directory not found")
            return geo_files
        
        for geo_file in geo_dir.glob("*.wld"):
            try:
                file_info = {
                    "filename": geo_file.name,
                    "file_size": geo_file.stat().st_size,
                    "file_type": "WLD"
                }
                
                # Read world file content
                with open(geo_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 6:
                        # World file format: pixel size, rotation, rotation, pixel size, x-coordinate, y-coordinate
                        file_info["pixel_size_x"] = float(lines[0].strip())
                        file_info["rotation_y"] = float(lines[1].strip())
                        file_info["rotation_x"] = float(lines[2].strip())
                        file_info["pixel_size_y"] = float(lines[3].strip())
                        file_info["x_coordinate"] = float(lines[4].strip())
                        file_info["y_coordinate"] = float(lines[5].strip())
                
                geo_files.append(file_info)
                logger.info(f"Successfully processed GEO file: {geo_file.name}")
                
            except Exception as e:
                logger.error(f"Error processing GEO file {geo_file.name}: {str(e)}")
                continue
        
        return geo_files
