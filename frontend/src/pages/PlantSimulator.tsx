import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Leaf, 
  Thermometer, 
  Droplets, 
  Sun, 
  Activity, 
  CheckCircle,
  AlertTriangle,
  Loader
} from 'lucide-react';

// Simple plant data simulator - minimal functionality
const PlantSimulator: React.FC = () => {
  const [plantType, setPlantType] = useState<string>('chili_pepper');
  const [temperature, setTemperature] = useState<number>(25.5);
  const [humidity, setHumidity] = useState<number>(65.0);
  const [soilMoisture, setSoilMoisture] = useState<number>(70.0);
  const [lightIntensity, setLightIntensity] = useState<number>(800.0);
  const [soilPh, setSoilPh] = useState<number>(6.5);
  const [status, setStatus] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  // Plant options
  const plantOptions = [
    { value: 'chili_pepper', label: 'Chili Pepper' },
    { value: 'grapevine', label: 'Grapevine' },
    { value: 'olive_tree', label: 'Olive Tree' }
  ];

  // Send data to backend
  const sendDataToBackend = async () => {
    setLoading(true);
    setStatus('');

    try {
      const response = await fetch('http://localhost:8000/plants/simulated-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plant_type: plantType,
          temperature: temperature,
          humidity: humidity,
          soil_moisture: soilMoisture,
          light_intensity: lightIntensity,
          soil_ph: soilPh
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setStatus(`Data sent successfully! Timestamp: ${new Date(data.timestamp).toLocaleString()}`);
      } else if (response.status === 404) {
        setStatus('Backend endpoint not found');
      } else {
        setStatus(`Error: ${response.status} - ${response.statusText}`);
      }
    } catch (error) {
      setStatus('Cannot connect to server');
      console.error('Network error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle slider change - send data immediately
  const handleSliderChange = (param: string, value: number) => {
    switch (param) {
      case 'temperature':
        setTemperature(value);
        break;
      case 'humidity':
        setHumidity(value);
        break;
      case 'soilMoisture':
        setSoilMoisture(value);
        break;
      case 'lightIntensity':
        setLightIntensity(value);
        break;
      case 'soilPh':
        setSoilPh(value);
        break;
    }
    
    // Send data immediately after slider change
    setTimeout(() => sendDataToBackend(), 100);
  };

  // Handle plant type change
  const handlePlantTypeChange = (value: string) => {
    setPlantType(value);
    // Send data immediately after plant type change
    setTimeout(() => sendDataToBackend(), 100);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-sky-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center">
            <Leaf className="w-10 h-10 text-emerald-600 mr-3" />
            🎚️ Simple Plant Data Simulator
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Adjust sliders to simulate plant sensor data and send to backend
          </p>
        </motion.div>

        {/* Main Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl shadow-lg p-8 max-w-4xl mx-auto"
        >
          {/* Plant Type Selection */}
          <div className="mb-8">
            <label className="block text-lg font-semibold text-gray-800 mb-4">
              Select Plant Type
            </label>
            <select
              value={plantType}
              onChange={(e) => handlePlantTypeChange(e.target.value)}
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-lg"
            >
              {plantOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Sliders */}
          <div className="space-y-8">
            {/* Temperature */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Thermometer className="w-6 h-6 text-red-500" />
                  <span className="text-lg font-medium text-gray-700">Temperature</span>
                </div>
                <span className="text-lg font-mono text-gray-600">
                  {temperature.toFixed(1)}°C
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="50"
                step="0.1"
                value={temperature}
                onChange={(e) => handleSliderChange('temperature', parseFloat(e.target.value))}
                className="w-full h-3 bg-gradient-to-r from-blue-200 to-red-400 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-sm text-gray-500">
                <span>0°C</span>
                <span>50°C</span>
              </div>
            </div>

            {/* Humidity */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Droplets className="w-6 h-6 text-blue-500" />
                  <span className="text-lg font-medium text-gray-700">Humidity</span>
                </div>
                <span className="text-lg font-mono text-gray-600">
                  {humidity.toFixed(1)}%
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="0.1"
                value={humidity}
                onChange={(e) => handleSliderChange('humidity', parseFloat(e.target.value))}
                className="w-full h-3 bg-gradient-to-r from-gray-200 to-blue-400 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-sm text-gray-500">
                <span>0%</span>
                <span>100%</span>
              </div>
            </div>

            {/* Soil Moisture */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Droplets className="w-6 h-6 text-green-500" />
                  <span className="text-lg font-medium text-gray-700">Soil Moisture</span>
                </div>
                <span className="text-lg font-mono text-gray-600">
                  {soilMoisture.toFixed(1)}%
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="0.1"
                value={soilMoisture}
                onChange={(e) => handleSliderChange('soilMoisture', parseFloat(e.target.value))}
                className="w-full h-3 bg-gradient-to-r from-yellow-200 to-green-400 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-sm text-gray-500">
                <span>0%</span>
                <span>100%</span>
              </div>
            </div>

            {/* Light Intensity */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Sun className="w-6 h-6 text-yellow-500" />
                  <span className="text-lg font-medium text-gray-700">Light Intensity</span>
                </div>
                <span className="text-lg font-mono text-gray-600">
                  {lightIntensity.toFixed(0)} lux
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="2000"
                step="10"
                value={lightIntensity}
                onChange={(e) => handleSliderChange('lightIntensity', parseFloat(e.target.value))}
                className="w-full h-3 bg-gradient-to-r from-gray-200 to-yellow-400 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-sm text-gray-500">
                <span>0 lux</span>
                <span>2000 lux</span>
              </div>
            </div>

            {/* Soil pH */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Activity className="w-6 h-6 text-purple-500" />
                  <span className="text-lg font-medium text-gray-700">Soil pH</span>
                </div>
                <span className="text-lg font-mono text-gray-600">
                  {soilPh.toFixed(1)} pH
                </span>
              </div>
              <input
                type="range"
                min="4.0"
                max="9.0"
                step="0.1"
                value={soilPh}
                onChange={(e) => handleSliderChange('soilPh', parseFloat(e.target.value))}
                className="w-full h-3 bg-gradient-to-r from-red-200 to-blue-400 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-sm text-gray-500">
                <span>4.0 pH</span>
                <span>9.0 pH</span>
              </div>
            </div>
          </div>

          {/* Status Message */}
          {status && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`mt-8 p-4 rounded-lg flex items-center ${
                status.includes('successfully') 
                  ? 'bg-green-50 border border-green-200 text-green-700'
                  : 'bg-red-50 border border-red-200 text-red-700'
              }`}
            >
              {status.includes('successfully') ? (
                <CheckCircle className="w-5 h-5 mr-2" />
              ) : (
                <AlertTriangle className="w-5 h-5 mr-2" />
              )}
              <span>{status}</span>
            </motion.div>
          )}

          {/* Loading Indicator */}
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 flex items-center justify-center text-gray-600"
            >
              <Loader className="w-5 h-5 mr-2 animate-spin" />
              <span>Sending data...</span>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default PlantSimulator;