import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union
from typing import List, Dict, Any, Tuple, Optional
import folium
from folium import plugins
import json
from datetime import datetime, timedelta
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from app.models.plant_models import PlantBloomEvent, BloomIntensity

class GeospatialAnalyzer:
    """Advanced geospatial analysis for bloom event detection and monitoring"""
    
    def __init__(self):
        self.crs = "EPSG:4326"  # WGS84 coordinate system
        self.earth_radius = 6371  # Earth radius in kilometers
    
    def create_bloom_gdf(self, events: List[PlantBloomEvent]) -> gpd.GeoDataFrame:
        """Convert bloom events to GeoDataFrame for spatial analysis"""
        data = []
        geometries = []
        
        for event in events:
            data.append({
                'id': event.id,
                'location': event.location,
                'region': event.region,
                'detection_date': event.detection_date,
                'intensity': event.intensity.value,
                'confidence': event.confidence,
                'vegetation_type': event.vegetation_type.value,
                'season': event.season.value,
                'satellite_source': event.satellite_source.value,
                'area_coverage': event.area_coverage,
                'duration_days': event.duration_days,
                'conservation_priority': event.conservation_priority
            })
            geometries.append(Point(event.longitude, event.latitude))
        
        gdf = gpd.GeoDataFrame(data, geometry=geometries, crs=self.crs)
        return gdf
    
    def detect_bloom_clusters(self, events: List[PlantBloomEvent], 
                           eps: float = 0.5, min_samples: int = 2) -> Dict[str, Any]:
        """Detect spatial clusters of bloom events using DBSCAN"""
        gdf = self.create_bloom_gdf(events)
        
        # Prepare coordinates for clustering
        coords = np.array([[point.x, point.y] for point in gdf.geometry])
        
        # Standardize coordinates
        scaler = StandardScaler()
        coords_scaled = scaler.fit_transform(coords)
        
        # Apply DBSCAN clustering
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coords_scaled)
        
        # Add cluster labels to GeoDataFrame
        gdf['cluster'] = clustering.labels_
        
        # Analyze clusters
        clusters = []
        for cluster_id in set(clustering.labels_):
            if cluster_id == -1:  # Noise points
                continue
            
            cluster_events = gdf[gdf['cluster'] == cluster_id]
            cluster_center = cluster_events.geometry.unary_union.centroid
            
            clusters.append({
                'cluster_id': cluster_id,
                'center_lat': cluster_center.y,
                'center_lon': cluster_center.x,
                'event_count': len(cluster_events),
                'avg_intensity': cluster_events['intensity'].mean(),
                'avg_confidence': cluster_events['confidence'].mean(),
                'total_area': cluster_events['area_coverage'].sum(),
                'regions': cluster_events['region'].unique().tolist(),
                'vegetation_types': cluster_events['vegetation_type'].unique().tolist()
            })
        
        return {
            'clusters': clusters,
            'noise_points': len(gdf[gdf['cluster'] == -1]),
            'total_clusters': len(clusters),
            'clustering_algorithm': 'DBSCAN',
            'parameters': {'eps': eps, 'min_samples': min_samples}
        }
    
    def calculate_bloom_density(self, events: List[PlantBloomEvent], 
                              grid_size: float = 1.0) -> Dict[str, Any]:
        """Calculate bloom density using spatial grid analysis"""
        gdf = self.create_bloom_gdf(events)
        
        # Create grid
        bounds = gdf.total_bounds
        minx, miny, maxx, maxy = bounds
        
        # Create grid cells
        x_coords = np.arange(minx, maxx + grid_size, grid_size)
        y_coords = np.arange(miny, maxy + grid_size, grid_size)
        
        grid_cells = []
        for i in range(len(x_coords) - 1):
            for j in range(len(y_coords) - 1):
                cell = Polygon([
                    (x_coords[i], y_coords[j]),
                    (x_coords[i + 1], y_coords[j]),
                    (x_coords[i + 1], y_coords[j + 1]),
                    (x_coords[i], y_coords[j + 1])
                ])
                grid_cells.append(cell)
        
        # Calculate density for each grid cell
        density_data = []
        for cell in grid_cells:
            # Count events in this cell
            events_in_cell = gdf[gdf.geometry.within(cell)]
            event_count = len(events_in_cell)
            
            if event_count > 0:
                density_data.append({
                    'geometry': cell,
                    'event_count': event_count,
                    'density': event_count / (grid_size * grid_size),
                    'avg_intensity': events_in_cell['intensity'].mean(),
                    'total_area': events_in_cell['area_coverage'].sum()
                })
        
        return {
            'grid_size': grid_size,
            'total_cells': len(grid_cells),
            'active_cells': len(density_data),
            'max_density': max([d['density'] for d in density_data]) if density_data else 0,
            'density_data': density_data
        }
    
    def analyze_temporal_patterns(self, events: List[PlantBloomEvent]) -> Dict[str, Any]:
        """Analyze temporal patterns in bloom events"""
        gdf = self.create_bloom_gdf(events)
        
        # Convert dates to pandas datetime
        gdf['date'] = pd.to_datetime(gdf['detection_date'])
        gdf['year'] = gdf['date'].dt.year
        gdf['month'] = gdf['date'].dt.month
        gdf['day_of_year'] = gdf['date'].dt.dayofyear
        
        # Temporal analysis
        yearly_counts = gdf.groupby('year').size().to_dict()
        monthly_counts = gdf.groupby('month').size().to_dict()
        seasonal_counts = gdf.groupby('season').size().to_dict()
        
        # Peak bloom periods
        peak_months = sorted(monthly_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Trend analysis
        years = sorted(yearly_counts.keys())
        counts = [yearly_counts[year] for year in years]
        
        # Simple trend calculation
        if len(years) > 1:
            trend_slope = np.polyfit(years, counts, 1)[0]
            trend_direction = "increasing" if trend_slope > 0 else "decreasing" if trend_slope < 0 else "stable"
        else:
            trend_slope = 0
            trend_direction = "insufficient_data"
        
        return {
            'yearly_counts': yearly_counts,
            'monthly_counts': monthly_counts,
            'seasonal_counts': seasonal_counts,
            'peak_months': peak_months,
            'trend_slope': trend_slope,
            'trend_direction': trend_direction,
            'total_events': len(events),
            'date_range': {
                'start': gdf['date'].min().isoformat(),
                'end': gdf['date'].max().isoformat()
            }
        }
    
    def create_interactive_map(self, events: List[PlantBloomEvent], 
                             map_center: Tuple[float, float] = (20.0, 0.0),
                             zoom_start: int = 2) -> str:
        """Create interactive Folium map with bloom events"""
        # Create base map
        m = folium.Map(
            location=map_center,
            zoom_start=zoom_start,
            tiles='OpenStreetMap'
        )
        
        # Add satellite imagery layer
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite Imagery',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Color mapping for intensity
        intensity_colors = {
            'low': 'green',
            'medium': 'orange', 
            'high': 'red'
        }
        
        # Add bloom event markers
        for event in events:
            color = intensity_colors.get(event.intensity.value, 'blue')
            
            # Create popup content
            popup_content = f"""
            <div style="width: 250px;">
                <h4>{event.location}</h4>
                <p><strong>Region:</strong> {event.region}</p>
                <p><strong>Intensity:</strong> {event.intensity.value.title()}</p>
                <p><strong>Confidence:</strong> {event.confidence}%</p>
                <p><strong>Date:</strong> {event.detection_date.strftime('%Y-%m-%d')}</p>
                <p><strong>Vegetation:</strong> {event.vegetation_type.value.title()}</p>
                <p><strong>Area:</strong> {event.area_coverage:.1f} km²</p>
                <p><strong>Duration:</strong> {event.duration_days} days</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[event.latitude, event.longitude],
                radius=8,
                popup=folium.Popup(popup_content, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
        
        # Add heatmap layer
        heat_data = [[event.latitude, event.longitude, event.confidence] for event in events]
        plugins.HeatMap(heat_data, name='Bloom Intensity Heatmap').add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Add clustering for better performance
        marker_cluster = plugins.MarkerCluster().add_to(m)
        
        # Add fullscreen button
        plugins.Fullscreen().add_to(m)
        
        # Add measure control
        plugins.MeasureControl().add_to(m)
        
        return m._repr_html_()
    
    def generate_conservation_priority_map(self, events: List[PlantBloomEvent]) -> str:
        """Generate conservation priority visualization"""
        # Filter high priority events
        high_priority_events = [e for e in events if e.conservation_priority and e.conservation_priority >= 4]
        
        if not high_priority_events:
            return self.create_interactive_map(events)
        
        # Create map centered on high priority areas
        if high_priority_events:
            center_lat = np.mean([e.latitude for e in high_priority_events])
            center_lon = np.mean([e.longitude for e in high_priority_events])
        else:
            center_lat, center_lon = 20.0, 0.0
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add all events with different styling based on priority
        for event in events:
            if event.conservation_priority and event.conservation_priority >= 4:
                color = 'red'
                size = 12
                weight = 3
            elif event.conservation_priority and event.conservation_priority >= 3:
                color = 'orange'
                size = 10
                weight = 2
            else:
                color = 'green'
                size = 8
                weight = 1
            
            folium.CircleMarker(
                location=[event.latitude, event.longitude],
                radius=size,
                popup=f"<b>{event.location}</b><br>Priority: {event.conservation_priority or 'N/A'}",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.6,
                weight=weight
            ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 90px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p><b>Conservation Priority</b></p>
        <p><i class="fa fa-circle" style="color:red"></i> High (4-5)</p>
        <p><i class="fa fa-circle" style="color:orange"></i> Medium (3)</p>
        <p><i class="fa fa-circle" style="color:green"></i> Low (1-2)</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m._repr_html_()
    
    def export_spatial_data(self, events: List[PlantBloomEvent], 
                          format: str = 'geojson') -> str:
        """Export spatial data in various formats"""
        gdf = self.create_bloom_gdf(events)
        
        if format.lower() == 'geojson':
            return gdf.to_json()
        elif format.lower() == 'csv':
            # Convert geometry to lat/lon columns
            gdf['latitude'] = gdf.geometry.y
            gdf['longitude'] = gdf.geometry.x
            return gdf.drop('geometry', axis=1).to_csv(index=False)
        elif format.lower() == 'kml':
            # For KML export, we'd need additional libraries
            # For now, return GeoJSON
            return gdf.to_json()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def calculate_spatial_statistics(self, events: List[PlantBloomEvent]) -> Dict[str, Any]:
        """Calculate comprehensive spatial statistics"""
        gdf = self.create_bloom_gdf(events)
        
        # Basic spatial statistics
        bounds = gdf.total_bounds
        centroid = gdf.geometry.centroid
        
        # Calculate distances between events
        distances = []
        for i, point1 in enumerate(gdf.geometry):
            for j, point2 in enumerate(gdf.geometry):
                if i < j:  # Avoid duplicate pairs
                    dist = point1.distance(point2) * 111  # Rough conversion to km
                    distances.append(dist)
        
        # Spatial distribution metrics
        if distances:
            avg_distance = np.mean(distances)
            min_distance = np.min(distances)
            max_distance = np.max(distances)
        else:
            avg_distance = min_distance = max_distance = 0
        
        # Regional distribution
        regional_counts = gdf['region'].value_counts().to_dict()
        
        # Vegetation type distribution
        vegetation_counts = gdf['vegetation_type'].value_counts().to_dict()
        
        return {
            'total_events': len(events),
            'spatial_bounds': {
                'min_lat': bounds[1],
                'max_lat': bounds[3],
                'min_lon': bounds[0],
                'max_lon': bounds[2]
            },
            'centroid': {
                'latitude': centroid.y.mean(),
                'longitude': centroid.x.mean()
            },
            'distance_metrics': {
                'average_distance_km': avg_distance,
                'minimum_distance_km': min_distance,
                'maximum_distance_km': max_distance
            },
            'regional_distribution': regional_counts,
            'vegetation_distribution': vegetation_counts,
            'spatial_extent_km': max_distance
        }
