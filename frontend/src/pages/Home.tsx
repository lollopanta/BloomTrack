import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Hero } from '../components/Hero';
import { DatasetCard } from '../components/DatasetCard';
import { DatasetInfo } from '../types';

const datasets: DatasetInfo[] = [
  {
    name: 'modis',
    displayName: 'MODIS Terra Vegetation Indices',
    description: 'Monitor vegetation health and growth patterns using NDVI and EVI indices from MODIS satellite data.',
    icon: '🌱',
    color: 'green',
    route: '/dataset/modis'
  },
  {
    name: 'merra',
    displayName: 'MERRA-2 Climate Data',
    description: 'Analyze atmospheric conditions, temperature, humidity, and climate patterns with NASA\'s MERRA-2 reanalysis data.',
    icon: '🌡️',
    color: 'blue',
    route: '/dataset/merra'
  },
  {
    name: 'alos',
    displayName: 'ALOS PALSAR Terrain Data',
    description: 'Study surface changes, terrain reflectivity, and radar backscatter using ALOS PALSAR synthetic aperture radar data.',
    icon: '🛰️',
    color: 'purple',
    route: '/dataset/alos'
  }
];

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleDatasetClick = (route: string) => {
    navigate(route);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-primary-50 to-indigo-50">
      {/* Hero Section */}
      <Hero />

      {/* Datasets Section */}
      <section data-section="datasets" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Section Header */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Explore Our <span className="bg-gradient-to-r from-primary-600 to-sky-600 bg-clip-text text-transparent">Datasets</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Access comprehensive satellite and climate data from multiple sources, 
              processed and ready for analysis with our advanced machine learning models.
            </p>
          </motion.div>

          {/* Dataset Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {datasets.map((dataset, index) => (
              <DatasetCard
                key={dataset.name}
                dataset={dataset}
                onClick={handleDatasetClick}
                index={index}
              />
            ))}
          </div>

          {/* CTA Section */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            viewport={{ once: true }}
            className="text-center mt-16"
          >
            <div className="bg-gradient-to-r from-primary-600 to-sky-600 rounded-3xl p-8 md:p-12 text-white">
              <h3 className="text-3xl md:text-4xl font-bold mb-4">
                Ready to Start Predicting?
              </h3>
              <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
                Join researchers and scientists worldwide in using our platform 
                to forecast environmental changes and make data-driven decisions.
              </p>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/datasets')}
                className="bg-white text-primary-600 px-8 py-4 rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300"
              >
                Get Started Now
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Why Choose <span className="text-primary-600">BloomTracker</span>?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our platform combines cutting-edge technology with user-friendly design 
              to deliver powerful environmental forecasting capabilities.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                title: 'Advanced ML Models',
                description: 'ARIMA, Prophet, and LSTM models for accurate predictions',
                icon: '🧠'
              },
              {
                title: 'Real-time Processing',
                description: 'Process and analyze data in real-time with our API',
                icon: '⚡'
              },
              {
                title: 'Interactive Visualizations',
                description: 'Beautiful charts and maps to explore your data',
                icon: '📊'
              },
              {
                title: 'Global Coverage',
                description: 'Monitor Earth from space with satellite data',
                icon: '🌍'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center p-6"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};
