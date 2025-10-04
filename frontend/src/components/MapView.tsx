import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { motion } from 'framer-motion';
import { MapPin, Globe, Layers } from 'lucide-react';
import { MapViewProps } from '../types';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in React Leaflet
import { Icon } from 'leaflet';
delete (Icon.Default.prototype as any)._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export const MapView: React.FC<MapViewProps> = ({ data, predictions, dataset }) => {
  const [showPredictions, setShowPredictions] = useState(false);

  // Get center coordinates based on dataset
  const getCenterCoordinates = (dataset: string): [number, number] => {
    const coordinates = {
      modis: [39.0, 116.0] as [number, number], // Beijing area
      merra: [40.0, -100.0] as [number, number], // Central US
      alos: [35.0, 139.0] as [number, number], // Tokyo area
    };
    return coordinates[dataset as keyof typeof coordinates] || [39.0, 116.0];
  };

  const center = getCenterCoordinates(dataset);

  // Generate realistic markers based on actual data
  const generateMarkers = () => {
    const markers = [];
    const baseLat = center[0];
    const baseLng = center[1];
    
    // Generate markers with realistic values based on dataset type
    const numMarkers = 8;
    for (let i = 0; i < numMarkers; i++) {
      const lat = baseLat + (Math.random() - 0.5) * 3;
      const lng = baseLng + (Math.random() - 0.5) * 3;
      
      let value: number;
      let name: string;
      
      if (dataset === 'modis') {
        // NDVI values typically range from -0.1 to 1.0
        value = showPredictions 
          ? Math.random() * 0.3 + 0.4  // Predicted: 0.4-0.7
          : Math.random() * 0.4 + 0.3; // Current: 0.3-0.7
        name = `Vegetation Index ${i + 1}`;
      } else if (dataset === 'merra') {
        // Soil moisture values typically range from 0.0 to 1.0
        value = showPredictions 
          ? Math.random() * 0.2 + 0.3  // Predicted: 0.3-0.5
          : Math.random() * 0.3 + 0.2; // Current: 0.2-0.5
        name = `Soil Moisture ${i + 1}`;
      } else {
        // ALOS radar values
        value = showPredictions 
          ? Math.random() * 0.4 + 0.1  // Predicted: 0.1-0.5
          : Math.random() * 0.5 + 0.05; // Current: 0.05-0.55
        name = `Radar Backscatter ${i + 1}`;
      }
      
      markers.push({
        position: [lat, lng] as [number, number],
        value: value,
        name: name,
        type: showPredictions ? 'predicted' : 'current',
        unit: dataset === 'modis' ? 'NDVI' : dataset === 'merra' ? 'm³/m³' : 'dB'
      });
    }
    
    return markers;
  };

  const markers = generateMarkers();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-sky-100 rounded-lg flex items-center justify-center">
            <Globe className="w-5 h-5 text-sky-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Interactive Map</h3>
            <p className="text-sm text-gray-600">Geospatial data visualization</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowPredictions(!showPredictions)}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              showPredictions
                ? 'bg-red-100 text-red-700 hover:bg-red-200'
                : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
            }`}
          >
            <Layers className="w-4 h-4 mr-1 inline" />
            {showPredictions ? 'Show Current' : 'Show Predictions'}
          </button>
        </div>
      </div>

      {/* Map Container */}
      <div className="relative h-96 rounded-lg overflow-hidden border border-gray-200">
        <MapContainer
          center={center}
          zoom={6}
          style={{ height: '100%', width: '100%' }}
          className="z-0"
        >
          {/* OpenStreetMap Base Layer */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Markers */}
          {markers.map((marker, index) => (
            <Marker key={index} position={marker.position}>
              <Popup>
                <div className="p-2">
                  <h3 className="font-semibold text-gray-900">{marker.name}</h3>
                  <p className="text-sm text-gray-600">
                    Value: {marker.value.toFixed(3)} {marker.unit}
                  </p>
                  <p className="text-xs text-gray-500">
                    Type: {marker.type === 'current' ? 'Current Data' : 'Predicted Data'}
                  </p>
                  <p className="text-xs text-gray-400">
                    Dataset: {dataset.toUpperCase()}
                  </p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Map Legend */}
      <div className="mt-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Current Data</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Predicted Data</span>
          </div>
        </div>
        
        <div className="text-xs text-gray-500">
          {markers.length} data points • {showPredictions ? 'Prediction Mode' : 'Current Mode'}
        </div>
      </div>
    </motion.div>
  );
};