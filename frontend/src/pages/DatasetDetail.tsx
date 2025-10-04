import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, RefreshCw, Settings, TrendingUp, MapPin, Database } from 'lucide-react';
import { Chart } from '../components/Chart';
import { MapView } from '../components/MapView';
import { Loader } from '../components/Loader';
import { getDatasetData, getPredictions } from '../api/bloomtracker';
import { DatasetData, PredictionData } from '../types';
import { cn } from '../utils';

export const DatasetDetail: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const navigate = useNavigate();
  
  const [datasetData, setDatasetData] = useState<DatasetData | null>(null);
  const [predictionData, setPredictionData] = useState<PredictionData | null>(null);
  const [selectedModel, setSelectedModel] = useState<string>('auto');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const models = [
    { value: 'auto', label: 'Auto Select' },
    { value: 'arima', label: 'ARIMA' },
    { value: 'prophet', label: 'Prophet' },
    { value: 'lstm', label: 'LSTM' }
  ];

  const fetchData = async () => {
    if (!name) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // Fetch dataset data
      const dataResponse = await getDatasetData(name);
      if (dataResponse.success) {
        setDatasetData(dataResponse.data);
      }
      
      // Fetch predictions
      const predictionResponse = await getPredictions(name, selectedModel);
      if (predictionResponse.success) {
        setPredictionData(predictionResponse.data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const handleModelChange = async (model: string) => {
    setSelectedModel(model);
    if (!name) return;
    
    try {
      const response = await getPredictions(name, model);
      if (response.success) {
        setPredictionData(response.data);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchData();
  }, [name]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader size="lg" text="Loading dataset..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Data</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Go Home
          </button>
        </div>
      </div>
    );
  }

  const getDatasetInfo = (name: string) => {
    const info = {
      modis: {
        title: 'MODIS Terra Vegetation Indices',
        description: 'Vegetation monitoring and health analysis',
        icon: '🌱',
        color: 'green'
      },
      merra: {
        title: 'MERRA-2 Climate Data',
        description: 'Atmospheric and climate analysis',
        icon: '🌡️',
        color: 'blue'
      },
      alos: {
        title: 'ALOS PALSAR Terrain Data',
        description: 'Radar terrain and surface analysis',
        icon: '🛰️',
        color: 'purple'
      }
    };
    return info[name as keyof typeof info] || info.modis;
  };

  const datasetInfo = getDatasetInfo(name || '');

  // Generate chart data
  const chartData = predictionData?.timestamps.map((timestamp, index) => ({
    timestamp,
    current: Math.random() * 100, // Mock current data
    predicted: predictionData.predicted_values[index]
  })) || [];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-gray-600" />
              </button>
              
              <div className="flex items-center space-x-3">
                <div className={cn(
                  'w-12 h-12 rounded-xl flex items-center justify-center text-2xl',
                  `bg-${datasetInfo.color}-100`
                )}>
                  {datasetInfo.icon}
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">{datasetInfo.title}</h1>
                  <p className="text-gray-600">{datasetInfo.description}</p>
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
              >
                <RefreshCw className={cn('w-4 h-4', refreshing && 'animate-spin')} />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dataset Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Database className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Total Files</p>
                <p className="text-2xl font-bold text-gray-900">{datasetData?.total_files || 0}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Model Used</p>
                <p className="text-2xl font-bold text-gray-900">{predictionData?.model_used || 'N/A'}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <MapPin className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Data Type</p>
                <p className="text-2xl font-bold text-gray-900">{datasetData?.data_type || 'Unknown'}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                <Settings className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Confidence</p>
                <p className="text-2xl font-bold text-gray-900">85%</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Model Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Prediction Model</h3>
            <p className="text-sm text-gray-600">Select a model to generate predictions</p>
          </div>
          
          <div className="flex flex-wrap gap-3">
            {models.map((model) => (
              <button
                key={model.value}
                onClick={() => handleModelChange(model.value)}
                className={cn(
                  'px-4 py-2 rounded-lg font-medium transition-colors',
                  selectedModel === model.value
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                )}
              >
                {model.label}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Charts and Map Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Chart */}
          <Chart
            data={chartData}
            currentData={chartData.map(d => d.current)}
            predictedData={chartData.map(d => d.predicted)}
            title={`${datasetInfo.title} Analysis`}
          />
          
          {/* Map */}
          <MapView
            data={datasetData}
            predictions={predictionData}
            dataset={name || ''}
          />
        </div>

        {/* Predictions Table */}
        {predictionData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mt-8"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Prediction Results</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Date</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Predicted Value</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Confidence</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-600">Model</th>
                  </tr>
                </thead>
                <tbody>
                  {predictionData.timestamps.map((timestamp, index) => (
                    <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4">{new Date(timestamp).toLocaleDateString()}</td>
                      <td className="py-3 px-4 font-medium">{predictionData.predicted_values[index]?.toFixed(2)}</td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                          High
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">{predictionData.model_used}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};
