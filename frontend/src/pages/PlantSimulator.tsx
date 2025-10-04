import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Leaf, 
  Thermometer, 
  Droplets, 
  Sun, 
  Activity, 
  Brain, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  RefreshCw,
  Settings,
  BarChart3
} from 'lucide-react';
import { cn } from '../utils';

// Types for plant sensor data
interface PlantSensorData {
  plant_type: string;
  temperature: number;
  humidity: number;
  soil_moisture: number;
  light_intensity: number;
  soil_ph: number;
  growth_stage: string;
  location: string;
  timestamp: string;
}

interface SensorReading {
  parameter: string;
  current_value: number;
  optimal_min: number;
  optimal_max: number;
  optimal_target: number;
  health_score: number;
  status: string;
  recommendation: string;
}

interface PlantAnalysis {
  plant_name: string;
  growth_stage: string;
  overall_health_score: number;
  overall_status: string;
  sensor_readings: SensorReading[];
  critical_issues: string[];
  recommendations: string[];
  ai_advice?: string;
  analysis_timestamp: string;
}

interface Plant {
  name: string;
  scientific_name: string;
  category: string;
  key: string;
}

const PlantSimulator: React.FC = () => {
  const [plants, setPlants] = useState<Plant[]>([]);
  const [selectedPlant, setSelectedPlant] = useState<string>('chili_pepper');
  const [growthStage, setGrowthStage] = useState<string>('vegetative');
  const [location, setLocation] = useState<string>('Indoor');
  const [sensorData, setSensorData] = useState<PlantSensorData | null>(null);
  const [analysis, setAnalysis] = useState<PlantAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sliderValues, setSliderValues] = useState({
    temperature: 23,
    humidity: 60,
    soil_moisture: 60,
    light_intensity: 600,
    soil_ph: 6.5
  });

  // Fetch available plants
  useEffect(() => {
    const fetchPlants = async () => {
      try {
        const response = await fetch('http://localhost:8000/plants/');
        if (!response.ok) throw new Error('Failed to fetch plants');
        const data = await response.json();
        setPlants(data);
      } catch (err) {
        setError('Failed to load plants');
        console.error('Error fetching plants:', err);
      }
    };

    fetchPlants();
  }, []);

  // Generate simulated data when plant or growth stage changes
  useEffect(() => {
    if (selectedPlant && growthStage) {
      generateSimulatedData();
    }
  }, [selectedPlant, growthStage, location]);

  const generateSimulatedData = async () => {
    try {
      setLoading(true);
      const response = await fetch(
        `http://localhost:8000/plants/simulated-data?plant_name=${selectedPlant}&growth_stage=${growthStage}&location=${location}`
      );
      if (!response.ok) throw new Error('Failed to generate simulated data');
      const data = await response.json();
      setSensorData(data);
      
      // Update slider values with simulated data
      setSliderValues({
        temperature: data.temperature,
        humidity: data.humidity,
        soil_moisture: data.soil_moisture,
        light_intensity: data.light_intensity,
        soil_ph: data.soil_ph
      });
    } catch (err) {
      setError('Failed to generate simulated data');
      console.error('Error generating simulated data:', err);
    } finally {
      setLoading(false);
    }
  };

  const analyzeSensorData = async () => {
    if (!sensorData) return;

    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/plants/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...sensorData,
          temperature: sliderValues.temperature,
          humidity: sliderValues.humidity,
          soil_moisture: sliderValues.soil_moisture,
          light_intensity: sliderValues.light_intensity,
          soil_ph: sliderValues.soil_ph,
        }),
      });

      if (!response.ok) throw new Error('Failed to analyze sensor data');
      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError('Failed to analyze sensor data');
      console.error('Error analyzing sensor data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getHealthStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'text-emerald-600 bg-emerald-50';
      case 'good': return 'text-blue-600 bg-blue-50';
      case 'warning': return 'text-yellow-600 bg-yellow-50';
      case 'critical': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getHealthStatusIcon = (status: string) => {
    switch (status) {
      case 'excellent': return <CheckCircle className="w-4 h-4" />;
      case 'good': return <CheckCircle className="w-4 h-4" />;
      case 'warning': return <AlertTriangle className="w-4 h-4" />;
      case 'critical': return <AlertTriangle className="w-4 h-4" />;
      default: return <Info className="w-4 h-4" />;
    }
  };

  const SensorSlider: React.FC<{
    label: string;
    icon: React.ReactNode;
    value: number;
    onChange: (value: number) => void;
    min: number;
    max: number;
    step: number;
    unit: string;
    optimalRange?: { min: number; max: number };
  }> = ({ label, icon, value, onChange, min, max, step, unit, optimalRange }) => {
    const isInOptimalRange = optimalRange ? 
      value >= optimalRange.min && value <= optimalRange.max : true;
    
    return (
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {icon}
            <span className="font-medium text-gray-700">{label}</span>
          </div>
          <span className="text-sm font-mono text-gray-600">
            {value.toFixed(1)} {unit}
          </span>
        </div>
        
        <div className="relative">
          <input
            type="range"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={(e) => onChange(parseFloat(e.target.value))}
            className={cn(
              "w-full h-2 rounded-lg appearance-none cursor-pointer",
              isInOptimalRange 
                ? "bg-gradient-to-r from-emerald-200 to-emerald-400" 
                : "bg-gradient-to-r from-red-200 to-red-400"
            )}
          />
          {optimalRange && (
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>{min}</span>
              <span className="text-emerald-600 font-medium">
                Optimal: {optimalRange.min}-{optimalRange.max}
              </span>
              <span>{max}</span>
            </div>
          )}
        </div>
      </div>
    );
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
            Plant Sensor Simulator
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Simulate plant sensor readings and get AI-powered gardening advice for optimal plant health
          </p>
        </motion.div>

        {/* Plant Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <Settings className="w-5 h-5 text-indigo-500 mr-2" />
            Plant Configuration
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Plant Type
              </label>
              <select
                value={selectedPlant}
                onChange={(e) => setSelectedPlant(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              >
                {plants.map((plant) => (
                  <option key={plant.key} value={plant.key}>
                    {plant.name} ({plant.scientific_name})
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Growth Stage
              </label>
              <select
                value={growthStage}
                onChange={(e) => setGrowthStage(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              >
                <option value="germination">Germination</option>
                <option value="vegetative">Vegetative</option>
                <option value="flowering">Flowering</option>
                <option value="fruiting">Fruiting</option>
                <option value="dormancy">Dormancy</option>
                <option value="bud_break">Bud Break</option>
                <option value="fruit_development">Fruit Development</option>
                <option value="ripening">Ripening</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <select
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              >
                <option value="Indoor">Indoor</option>
                <option value="Greenhouse">Greenhouse</option>
                <option value="Outdoor">Outdoor</option>
              </select>
            </div>
          </div>
          
          <div className="mt-4 flex justify-end">
            <button
              onClick={generateSimulatedData}
              disabled={loading}
              className="flex items-center px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50"
            >
              <RefreshCw className={cn("w-4 h-4 mr-2", loading && "animate-spin")} />
              Generate Simulated Data
            </button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Sensor Controls */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl shadow-lg p-6"
          >
            <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center">
              <BarChart3 className="w-5 h-5 text-indigo-500 mr-2" />
              Sensor Controls
            </h2>
            
            <div className="space-y-6">
              <SensorSlider
                label="Temperature"
                icon={<Thermometer className="w-5 h-5 text-red-500" />}
                value={sliderValues.temperature}
                onChange={(value) => setSliderValues(prev => ({ ...prev, temperature: value }))}
                min={0}
                max={50}
                step={0.1}
                unit="°C"
                optimalRange={analysis?.sensor_readings.find(r => r.parameter === 'temperature') ? {
                  min: analysis.sensor_readings.find(r => r.parameter === 'temperature')!.optimal_min,
                  max: analysis.sensor_readings.find(r => r.parameter === 'temperature')!.optimal_max
                } : undefined}
              />
              
              <SensorSlider
                label="Humidity"
                icon={<Droplets className="w-5 h-5 text-blue-500" />}
                value={sliderValues.humidity}
                onChange={(value) => setSliderValues(prev => ({ ...prev, humidity: value }))}
                min={0}
                max={100}
                step={1}
                unit="%"
                optimalRange={analysis?.sensor_readings.find(r => r.parameter === 'humidity') ? {
                  min: analysis.sensor_readings.find(r => r.parameter === 'humidity')!.optimal_min,
                  max: analysis.sensor_readings.find(r => r.parameter === 'humidity')!.optimal_max
                } : undefined}
              />
              
              <SensorSlider
                label="Soil Moisture"
                icon={<Droplets className="w-5 h-5 text-green-500" />}
                value={sliderValues.soil_moisture}
                onChange={(value) => setSliderValues(prev => ({ ...prev, soil_moisture: value }))}
                min={0}
                max={100}
                step={1}
                unit="%"
                optimalRange={analysis?.sensor_readings.find(r => r.parameter === 'soil_moisture') ? {
                  min: analysis.sensor_readings.find(r => r.parameter === 'soil_moisture')!.optimal_min,
                  max: analysis.sensor_readings.find(r => r.parameter === 'soil_moisture')!.optimal_max
                } : undefined}
              />
              
              <SensorSlider
                label="Light Intensity"
                icon={<Sun className="w-5 h-5 text-yellow-500" />}
                value={sliderValues.light_intensity}
                onChange={(value) => setSliderValues(prev => ({ ...prev, light_intensity: value }))}
                min={0}
                max={2000}
                step={10}
                unit="lux"
                optimalRange={analysis?.sensor_readings.find(r => r.parameter === 'light_intensity') ? {
                  min: analysis.sensor_readings.find(r => r.parameter === 'light_intensity')!.optimal_min,
                  max: analysis.sensor_readings.find(r => r.parameter === 'light_intensity')!.optimal_max
                } : undefined}
              />
              
              <SensorSlider
                label="Soil pH"
                icon={<Activity className="w-5 h-5 text-purple-500" />}
                value={sliderValues.soil_ph}
                onChange={(value) => setSliderValues(prev => ({ ...prev, soil_ph: value }))}
                min={4}
                max={9}
                step={0.1}
                unit="pH"
                optimalRange={analysis?.sensor_readings.find(r => r.parameter === 'soil_ph') ? {
                  min: analysis.sensor_readings.find(r => r.parameter === 'soil_ph')!.optimal_min,
                  max: analysis.sensor_readings.find(r => r.parameter === 'soil_ph')!.optimal_max
                } : undefined}
              />
            </div>
            
            <div className="mt-6">
              <button
                onClick={analyzeSensorData}
                disabled={loading}
                className="w-full flex items-center justify-center px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
              >
                <Brain className={cn("w-5 h-5 mr-2", loading && "animate-pulse")} />
                {loading ? 'Analyzing...' : 'Analyze Plant Health'}
              </button>
            </div>
          </motion.div>

          {/* Analysis Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            {/* Overall Health Score */}
            {analysis && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <Activity className="w-5 h-5 text-indigo-500 mr-2" />
                  Overall Health Score
                </h3>
                
                <div className="text-center mb-4">
                  <div className="text-4xl font-bold text-gray-900 mb-2">
                    {(analysis.overall_health_score * 100).toFixed(1)}%
                  </div>
                  <div className={cn(
                    "inline-flex items-center px-3 py-1 rounded-full text-sm font-medium",
                    getHealthStatusColor(analysis.overall_status)
                  )}>
                    {getHealthStatusIcon(analysis.overall_status)}
                    <span className="ml-1 capitalize">{analysis.overall_status}</span>
                  </div>
                </div>
                
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={cn(
                      "h-3 rounded-full transition-all duration-500",
                      analysis.overall_health_score >= 0.8 ? "bg-emerald-500" :
                      analysis.overall_health_score >= 0.6 ? "bg-blue-500" :
                      analysis.overall_health_score >= 0.4 ? "bg-yellow-500" : "bg-red-500"
                    )}
                    style={{ width: `${analysis.overall_health_score * 100}%` }}
                  />
                </div>
              </div>
            )}

            {/* Sensor Readings */}
            {analysis && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Sensor Analysis
                </h3>
                
                <div className="space-y-3">
                  {analysis.sensor_readings.map((reading, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className={cn(
                          "w-3 h-3 rounded-full",
                          reading.status === 'excellent' ? "bg-emerald-500" :
                          reading.status === 'good' ? "bg-blue-500" :
                          reading.status === 'warning' ? "bg-yellow-500" : "bg-red-500"
                        )} />
                        <span className="font-medium text-gray-700 capitalize">
                          {reading.parameter.replace('_', ' ')}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="font-mono text-sm text-gray-600">
                          {reading.current_value.toFixed(1)}
                        </div>
                        <div className="text-xs text-gray-500">
                          {reading.optimal_min}-{reading.optimal_max}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Critical Issues & Recommendations */}
            {analysis && (analysis.critical_issues.length > 0 || analysis.recommendations.length > 0) && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Issues & Recommendations
                </h3>
                
                {analysis.critical_issues.length > 0 && (
                  <div className="mb-4">
                    <h4 className="text-sm font-medium text-red-600 mb-2">Critical Issues</h4>
                    <ul className="space-y-1">
                      {analysis.critical_issues.map((issue, index) => (
                        <li key={index} className="text-sm text-red-600 flex items-start">
                          <AlertTriangle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                          {issue}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {analysis.recommendations.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-blue-600 mb-2">Recommendations</h4>
                    <ul className="space-y-1">
                      {analysis.recommendations.map((rec, index) => (
                        <li key={index} className="text-sm text-blue-600 flex items-start">
                          <CheckCircle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* AI Advice */}
            {analysis?.ai_advice && (
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <Brain className="w-5 h-5 text-purple-500 mr-2" />
                  AI Gardening Advice
                </h3>
                <div className="prose prose-sm max-w-none">
                  <p className="text-gray-700 leading-relaxed">
                    {analysis.ai_advice}
                  </p>
                </div>
              </div>
            )}
          </motion.div>
        </div>

        {/* Error Display */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8 bg-red-50 border border-red-200 rounded-lg p-4"
          >
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 text-red-500 mr-2" />
              <span className="text-red-700">{error}</span>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default PlantSimulator;
