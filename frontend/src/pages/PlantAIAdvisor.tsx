import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Leaf, 
  Thermometer, 
  Droplets, 
  Sun, 
  Zap, 
  Brain, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  MessageCircle,
  Settings,
  BarChart3
} from 'lucide-react';

// Types
interface PlantType {
  id: string;
  name: string;
  image: string;
  description: string;
  optimalConditions: {
    temperature: { min: number; max: number; optimal: number };
    humidity: { min: number; max: number; optimal: number };
    soilMoisture: { min: number; max: number; optimal: number };
    lightIntensity: { min: number; max: number; optimal: number };
    soilPh: { min: number; max: number; optimal: number };
  };
}

interface SensorData {
  temperature: number;
  humidity: number;
  soilMoisture: number;
  lightIntensity: number;
  soilPh: number;
  growthStage: string;
  location: string;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface HealthScore {
  overall: number;
  parameters: {
    temperature: number;
    humidity: number;
    soilMoisture: number;
    lightIntensity: number;
    soilPh: number;
  };
  criticalIssues: string[];
  recommendations: string[];
}

// Plant data
const PLANTS: PlantType[] = [
  {
    id: 'chili_pepper',
    name: 'Chili Pepper',
    image: '/api/placeholder/300/200',
    description: 'Spicy and vibrant, perfect for indoor growing',
    optimalConditions: {
      temperature: { min: 20, max: 30, optimal: 25 },
      humidity: { min: 40, max: 70, optimal: 60 },
      soilMoisture: { min: 50, max: 80, optimal: 65 },
      lightIntensity: { min: 6000, max: 12000, optimal: 9000 },
      soilPh: { min: 6.0, max: 7.0, optimal: 6.5 }
    }
  },
  {
    id: 'grapevine',
    name: 'Grapevine',
    image: '/api/placeholder/300/200',
    description: 'Elegant and productive, ideal for outdoor cultivation',
    optimalConditions: {
      temperature: { min: 15, max: 35, optimal: 25 },
      humidity: { min: 30, max: 60, optimal: 45 },
      soilMoisture: { min: 40, max: 70, optimal: 55 },
      lightIntensity: { min: 8000, max: 15000, optimal: 12000 },
      soilPh: { min: 6.0, max: 7.5, optimal: 6.8 }
    }
  },
  {
    id: 'olive_tree',
    name: 'Olive Tree',
    image: '/api/placeholder/300/200',
    description: 'Mediterranean beauty, perfect for sunny locations',
    optimalConditions: {
      temperature: { min: 10, max: 40, optimal: 25 },
      humidity: { min: 20, max: 50, optimal: 35 },
      soilMoisture: { min: 30, max: 60, optimal: 45 },
      lightIntensity: { min: 10000, max: 20000, optimal: 15000 },
      soilPh: { min: 6.5, max: 8.0, optimal: 7.2 }
    }
  }
];

// Component: Plant Selection Card
const PlantCard: React.FC<{
  plant: PlantType;
  isSelected: boolean;
  onClick: () => void;
}> = ({ plant, isSelected, onClick }) => (
  <motion.div
    className={`relative overflow-hidden rounded-2xl cursor-pointer transition-all duration-300 ${
      isSelected 
        ? 'ring-4 ring-green-500 shadow-2xl scale-105' 
        : 'hover:shadow-xl hover:scale-102'
    }`}
    onClick={onClick}
    whileHover={{ y: -5 }}
    whileTap={{ scale: 0.98 }}
  >
    <div className="aspect-video bg-gradient-to-br from-green-400 to-green-600 relative">
      <div className="absolute inset-0 bg-black/20" />
      <div className="absolute bottom-4 left-4 text-white">
        <h3 className="text-xl font-bold">{plant.name}</h3>
        <p className="text-sm opacity-90">{plant.description}</p>
      </div>
      {isSelected && (
        <motion.div
          className="absolute top-4 right-4"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 500 }}
        >
          <CheckCircle className="w-8 h-8 text-green-500" />
        </motion.div>
      )}
    </div>
  </motion.div>
);

// Component: Parameter Gauge
const ParameterGauge: React.FC<{
  label: string;
  value: number;
  optimal: { min: number; max: number; optimal: number };
  unit: string;
  icon: React.ReactNode;
}> = ({ label, value, optimal, unit, icon }) => {
  const getScore = (val: number, range: { min: number; max: number; optimal: number }) => {
    if (val >= range.min && val <= range.max) {
      const distanceFromOptimal = Math.abs(val - range.optimal);
      const rangeSize = range.max - range.min;
      return Math.max(0, 100 - (distanceFromOptimal / (rangeSize / 2)) * 50);
    }
    return Math.max(0, 50 - Math.abs(val - (val < range.min ? range.min : range.max)) * 10);
  };

  const score = getScore(value, optimal);
  const isGood = score >= 80;
  const isWarning = score >= 60 && score < 80;
  const isCritical = score < 60;

  return (
    <motion.div
      className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
      whileHover={{ y: -2 }}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${
            isGood ? 'bg-green-100 text-green-600' :
            isWarning ? 'bg-yellow-100 text-yellow-600' :
            'bg-red-100 text-red-600'
          }`}>
            {icon}
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">{label}</h3>
            <p className="text-sm text-gray-500">Optimal: {optimal.min}-{optimal.max}{unit}</p>
          </div>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
          isGood ? 'bg-green-100 text-green-800' :
          isWarning ? 'bg-yellow-100 text-yellow-800' :
          'bg-red-100 text-red-800'
        }`}>
          {Math.round(score)}%
        </div>
      </div>
      
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-gray-600">
          <span>{optimal.min}{unit}</span>
          <span className="font-medium">{value}{unit}</span>
          <span>{optimal.max}{unit}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className={`h-2 rounded-full ${
              isGood ? 'bg-green-500' :
              isWarning ? 'bg-yellow-500' :
              'bg-red-500'
            }`}
            style={{ width: `${Math.min(100, Math.max(0, (value - optimal.min) / (optimal.max - optimal.min) * 100))}%` }}
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(100, Math.max(0, (value - optimal.min) / (optimal.max - optimal.min) * 100))}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>
    </motion.div>
  );
};

// Component: Health Score Display
const HealthScore: React.FC<{ healthScore: HealthScore }> = ({ healthScore }) => (
  <motion.div
    className="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-8 text-center"
    initial={{ scale: 0.9, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    transition={{ duration: 0.5 }}
  >
    <div className="mb-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Plant Health Score</h2>
      <div className="relative inline-block">
        <motion.div
          className="w-32 h-32 rounded-full border-8 border-gray-200 flex items-center justify-center"
          initial={{ rotate: 0 }}
          animate={{ rotate: 360 }}
          transition={{ duration: 1, ease: "easeOut" }}
        >
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{healthScore.overall}</div>
            <div className="text-sm text-gray-600">/ 100</div>
          </div>
        </motion.div>
        <motion.div
          className="absolute inset-0 rounded-full border-8 border-green-500"
          style={{
            background: `conic-gradient(from 0deg, #10b981 0deg, #10b981 ${healthScore.overall * 3.6}deg, #e5e7eb ${healthScore.overall * 3.6}deg)`
          }}
          initial={{ rotate: 0 }}
          animate={{ rotate: 360 }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </div>
    </div>
    
    {healthScore.criticalIssues.length > 0 && (
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-red-600 mb-2">Critical Issues</h3>
        <div className="space-y-1">
          {healthScore.criticalIssues.map((issue, index) => (
            <div key={index} className="flex items-center space-x-2 text-red-600">
              <AlertTriangle className="w-4 h-4" />
              <span className="text-sm">{issue}</span>
            </div>
          ))}
        </div>
      </div>
    )}
    
    {healthScore.recommendations.length > 0 && (
      <div>
        <h3 className="text-lg font-semibold text-green-600 mb-2">Recommendations</h3>
        <div className="space-y-1">
          {healthScore.recommendations.map((rec, index) => (
            <div key={index} className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="w-4 h-4" />
              <span className="text-sm">{rec}</span>
            </div>
          ))}
        </div>
      </div>
    )}
  </motion.div>
);

// Component: AI Chat Interface
const AIChat: React.FC<{
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}> = ({ messages, onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(true);

  const suggestedQuestions = [
    "Why are my leaves turning yellow?",
    "How often should I water my plant?",
    "What's the best fertilizer for my plant?",
    "How can I improve my plant's health?",
    "What's causing the brown spots on my leaves?"
  ];

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
      setShowSuggestions(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 h-96 flex flex-col">
      <div className="p-4 border-b border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
          <Brain className="w-5 h-5 text-green-600" />
          <span>AI Garden Advisor</span>
        </h3>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                message.role === 'user'
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}>
                <p className="text-sm">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {isLoading && (
          <motion.div
            className="flex justify-start"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="bg-gray-100 rounded-2xl px-4 py-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              </div>
            </div>
          </motion.div>
        )}
      </div>
      
      {showSuggestions && messages.length === 0 && (
        <div className="p-4 border-t border-gray-100">
          <p className="text-sm text-gray-600 mb-3">Suggested questions:</p>
          <div className="space-y-2">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => {
                  setInput(question);
                  handleSend();
                }}
                className="w-full text-left p-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
      
      <div className="p-4 border-t border-gray-100">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about your plant..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <MessageCircle className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

// Component: Parameter Sliders
const ParameterSliders: React.FC<{
  conditions: SensorData;
  onUpdate: (conditions: SensorData) => void;
}> = ({ conditions, onUpdate }) => {
  const updateParameter = (key: keyof SensorData, value: number) => {
    onUpdate({ ...conditions, [key]: value });
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center space-x-2">
        <Settings className="w-5 h-5 text-green-600" />
        <span>Simulate Sensor Data</span>
      </h3>
      
      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Temperature: {conditions.temperature}°C
          </label>
          <input
            type="range"
            min="0"
            max="50"
            step="0.1"
            value={conditions.temperature}
            onChange={(e) => updateParameter('temperature', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Humidity: {conditions.humidity}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={conditions.humidity}
            onChange={(e) => updateParameter('humidity', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Soil Moisture: {conditions.soilMoisture}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            step="1"
            value={conditions.soilMoisture}
            onChange={(e) => updateParameter('soilMoisture', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Light Intensity: {conditions.lightIntensity} lux
          </label>
          <input
            type="range"
            min="0"
            max="20000"
            step="100"
            value={conditions.lightIntensity}
            onChange={(e) => updateParameter('lightIntensity', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Soil pH: {conditions.soilPh}
          </label>
          <input
            type="range"
            min="4"
            max="9"
            step="0.1"
            value={conditions.soilPh}
            onChange={(e) => updateParameter('soilPh', parseFloat(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Growth Stage</label>
            <select
              value={conditions.growthStage}
              onChange={(e) => updateParameter('growthStage', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="seedling">Seedling</option>
              <option value="vegetative">Vegetative</option>
              <option value="flowering">Flowering</option>
              <option value="fruiting">Fruiting</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <select
              value={conditions.location}
              onChange={(e) => updateParameter('location', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="indoor">Indoor</option>
              <option value="outdoor">Outdoor</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main Component
const PlantAIAdvisor: React.FC = () => {
  const [selectedPlant, setSelectedPlant] = useState<PlantType | null>(null);
  const [currentConditions, setCurrentConditions] = useState<SensorData>({
    temperature: 25,
    humidity: 60,
    soilMoisture: 65,
    lightIntensity: 9000,
    soilPh: 6.5,
    growthStage: 'vegetative',
    location: 'indoor'
  });
  const [healthScore, setHealthScore] = useState<HealthScore>({
    overall: 85,
    parameters: {
      temperature: 90,
      humidity: 80,
      soilMoisture: 85,
      lightIntensity: 90,
      soilPh: 85
    },
    criticalIssues: [],
    recommendations: []
  });
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Calculate health score when conditions change
  useEffect(() => {
    if (selectedPlant) {
      // Simulate health score calculation
      const calculateScore = (value: number, optimal: { min: number; max: number; optimal: number }) => {
        if (value >= optimal.min && value <= optimal.max) {
          const distanceFromOptimal = Math.abs(value - optimal.optimal);
          const rangeSize = optimal.max - optimal.min;
          return Math.max(0, 100 - (distanceFromOptimal / (rangeSize / 2)) * 50);
        }
        return Math.max(0, 50 - Math.abs(value - (value < optimal.min ? optimal.min : optimal.max)) * 10);
      };

      const tempScore = calculateScore(currentConditions.temperature, selectedPlant.optimalConditions.temperature);
      const humidityScore = calculateScore(currentConditions.humidity, selectedPlant.optimalConditions.humidity);
      const moistureScore = calculateScore(currentConditions.soilMoisture, selectedPlant.optimalConditions.soilMoisture);
      const lightScore = calculateScore(currentConditions.lightIntensity, selectedPlant.optimalConditions.lightIntensity);
      const phScore = calculateScore(currentConditions.soilPh, selectedPlant.optimalConditions.soilPh);

      const overall = Math.round((tempScore + humidityScore + moistureScore + lightScore + phScore) / 5);
      
      const criticalIssues = [];
      const recommendations = [];

      if (tempScore < 60) criticalIssues.push('Temperature outside optimal range');
      if (humidityScore < 60) criticalIssues.push('Humidity outside optimal range');
      if (moistureScore < 60) criticalIssues.push('Soil moisture outside optimal range');
      if (lightScore < 60) criticalIssues.push('Light intensity outside optimal range');
      if (phScore < 60) criticalIssues.push('Soil pH outside optimal range');

      setHealthScore({
        overall,
        parameters: {
          temperature: tempScore,
          humidity: humidityScore,
          soilMoisture: moistureScore,
          lightIntensity: lightScore,
          soilPh: phScore
        },
        criticalIssues,
        recommendations
      });
    }
  }, [selectedPlant, currentConditions]);

  const handleSendMessage = async (message: string) => {
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    setChatMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Based on your ${selectedPlant?.name} plant's current conditions, I can help you with that! Your plant has a health score of ${healthScore.overall}%. ${healthScore.criticalIssues.length > 0 ? `I notice some issues: ${healthScore.criticalIssues.join(', ')}.` : 'Your plant is doing well!'} Let me provide some specific advice for your situation.`,
        timestamp: new Date().toISOString()
      };

      setChatMessages(prev => [...prev, aiMessage]);
      setIsLoading(false);
    }, 2000);
  };

  if (!selectedPlant) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 py-12">
        <div className="max-w-6xl mx-auto px-4">
          <motion.div
            className="text-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center space-x-3">
              <Leaf className="w-10 h-10 text-green-600" />
              <span>Plant AI Advisor</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get personalized AI-powered gardening advice for your plants. Select a plant to get started!
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {PLANTS.map((plant, index) => (
              <motion.div
                key={plant.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <PlantCard
                  plant={plant}
                  isSelected={false}
                  onClick={() => setSelectedPlant(plant)}
                />
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center space-x-3">
                <Leaf className="w-8 h-8 text-green-600" />
                <span>{selectedPlant.name} AI Advisor</span>
              </h1>
              <p className="text-gray-600 mt-2">Real-time plant health monitoring and AI-powered advice</p>
            </div>
            <button
              onClick={() => setSelectedPlant(null)}
              className="px-4 py-2 bg-white text-gray-600 rounded-lg hover:bg-gray-50 transition-colors border border-gray-200"
            >
              Change Plant
            </button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Health Score and Parameters */}
          <div className="lg:col-span-2 space-y-8">
            {/* Health Score */}
            <HealthScore healthScore={healthScore} />

            {/* Parameter Gauges */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ParameterGauge
                label="Temperature"
                value={currentConditions.temperature}
                optimal={selectedPlant.optimalConditions.temperature}
                unit="°C"
                icon={<Thermometer className="w-5 h-5" />}
              />
              <ParameterGauge
                label="Humidity"
                value={currentConditions.humidity}
                optimal={selectedPlant.optimalConditions.humidity}
                unit="%"
                icon={<Droplets className="w-5 h-5" />}
              />
              <ParameterGauge
                label="Soil Moisture"
                value={currentConditions.soilMoisture}
                optimal={selectedPlant.optimalConditions.soilMoisture}
                unit="%"
                icon={<Droplets className="w-5 h-5" />}
              />
              <ParameterGauge
                label="Light Intensity"
                value={currentConditions.lightIntensity}
                optimal={selectedPlant.optimalConditions.lightIntensity}
                unit=" lux"
                icon={<Sun className="w-5 h-5" />}
              />
              <ParameterGauge
                label="Soil pH"
                value={currentConditions.soilPh}
                optimal={selectedPlant.optimalConditions.soilPh}
                unit=""
                icon={<Zap className="w-5 h-5" />}
              />
            </div>

            {/* Parameter Sliders */}
            <ParameterSliders
              conditions={currentConditions}
              onUpdate={setCurrentConditions}
            />
          </div>

          {/* Right Column - AI Chat */}
          <div className="lg:col-span-1">
            <AIChat
              messages={chatMessages}
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlantAIAdvisor;
