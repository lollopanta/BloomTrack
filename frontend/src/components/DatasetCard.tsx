import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Database, Globe, Radar } from 'lucide-react';
import { DatasetInfo } from '../types';
import { cn } from '../utils';

interface DatasetCardProps {
  dataset: DatasetInfo;
  onClick: (dataset: string) => void;
  index: number;
}

const getDatasetIcon = (name: string) => {
  switch (name.toLowerCase()) {
    case 'modis':
      return <Globe className="w-8 h-8" />;
    case 'merra':
      return <Database className="w-8 h-8" />;
    case 'alos':
      return <Radar className="w-8 h-8" />;
    default:
      return <Database className="w-8 h-8" />;
  }
};

export const DatasetCard: React.FC<DatasetCardProps> = ({ dataset, onClick, index }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      whileHover={{ y: -8, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => onClick(dataset.route)}
      className={cn(
        'group relative bg-white rounded-2xl p-8 shadow-lg border border-gray-100 cursor-pointer transition-all duration-300 hover:shadow-2xl overflow-hidden',
        `hover:border-${dataset.color}-200`
      )}
    >
      {/* Background Gradient */}
      <div 
        className={cn(
          'absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-300',
          `bg-gradient-to-br from-${dataset.color}-400 to-${dataset.color}-600`
        )}
      />
      
      {/* Content */}
      <div className="relative z-10">
        {/* Icon */}
        <motion.div
          whileHover={{ rotate: 360 }}
          transition={{ duration: 0.6 }}
          className={cn(
            'w-16 h-16 rounded-2xl flex items-center justify-center mb-6 transition-colors duration-300',
            `bg-${dataset.color}-100 text-${dataset.color}-600 group-hover:bg-${dataset.color}-600 group-hover:text-white`
          )}
        >
          {getDatasetIcon(dataset.name)}
        </motion.div>

        {/* Title */}
        <h3 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-gray-800 transition-colors">
          {dataset.displayName}
        </h3>

        {/* Description */}
        <p className="text-gray-600 mb-6 leading-relaxed group-hover:text-gray-700 transition-colors">
          {dataset.description}
        </p>

        {/* CTA Button */}
        <motion.div
          whileHover={{ x: 5 }}
          className="flex items-center space-x-2 text-primary-600 font-semibold group-hover:text-primary-700 transition-colors"
        >
          <span>View Data</span>
          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </motion.div>
      </div>

      {/* Hover Effect Border */}
      <div 
        className={cn(
          'absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-current transition-all duration-300',
          `group-hover:border-${dataset.color}-300`
        )}
      />
    </motion.div>
  );
};
