import React from 'react';
import { motion } from 'framer-motion';
import { Globe, TrendingUp, Zap, Database, Satellite, Brain, Users, Award, Rocket } from 'lucide-react';

export const About: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-primary-50 to-indigo-50">
      {/* Hero Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            {/* CyberHive Logo */}
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="flex justify-center mb-8"
            >
              <img 
                src="/src/images/cyberhive_logo.svg" 
                alt="CyberHive Logo" 
                className="w-32 h-32"
              />
            </motion.div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              About <span className="bg-gradient-to-r from-emerald-600 to-sky-600 bg-clip-text text-transparent">BloomTracker</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
              BloomTracker is a project developed for the <strong className="text-emerald-600">NASA International Space Apps Challenge 2025</strong>, 
              created by the <strong className="text-emerald-600">CyberHive team</strong>.
            </p>
            <p className="text-lg text-gray-600 max-w-4xl mx-auto leading-relaxed">
              It combines geospatial intelligence and machine learning to analyze and predict environmental trends 
              from satellite data (MODIS, MERRA-2, ALOS PALSAR). Our platform harnesses the power of AI-driven 
              analytics to forecast vegetation, climate, and terrain changes with unprecedented accuracy.
            </p>
          </motion.div>
        </div>
      </section>

      {/* NASA Space Apps Section */}
      <section className="py-20 bg-gradient-to-r from-emerald-50 to-sky-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <div className="flex items-center justify-center mb-6">
              <Award className="w-12 h-12 text-emerald-600 mr-4" />
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900">
                NASA Space Apps Challenge 2025
              </h2>
            </div>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Part of the world's largest global hackathon, bringing together coders, scientists, 
              designers, storytellers, makers, builders, and technologists to solve challenges 
              using NASA's open data.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: 'Global Impact',
                description: 'Join thousands of participants worldwide in solving Earth\'s challenges',
                icon: <Globe className="w-8 h-8" />,
                color: 'emerald'
              },
              {
                title: 'NASA Data',
                description: 'Access to NASA\'s vast collection of Earth observation data',
                icon: <Satellite className="w-8 h-8" />,
                color: 'sky'
              },
              {
                title: 'Innovation',
                description: 'Push the boundaries of what\'s possible with space technology',
                icon: <Rocket className="w-8 h-8" />,
                color: 'indigo'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-2xl p-8 text-center shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className={`text-${feature.color}-600 mb-4 flex justify-center`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
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

      {/* CyberHive Team Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <div className="flex items-center justify-center mb-6">
              <Users className="w-12 h-12 text-emerald-600 mr-4" />
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900">
                The CyberHive Team
              </h2>
            </div>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              A passionate team of developers, data scientists, and environmental enthusiasts 
              dedicated to using technology for the betterment of our planet.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
            {[
              { name: 'Lorenzo Pantalone', role: 'Lead Developer', expertise: 'Full-Stack Development' },
              { name: 'Francesco Mazzon', role: 'Developer', expertise: 'API Development' },
              { name: 'Matteo Conte', role: 'Developer', expertise: 'JSON Data Management' },
              { name: 'Camilla Carlucci', role: 'Designer', expertise: 'Exposition & design' },
              { name: 'Claudio Piccioni', role: 'Data Scientist', expertise: 'Info Researcher' }
            ].map((member, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gradient-to-br from-emerald-50 to-sky-50 rounded-2xl p-6 text-center hover:shadow-lg transition-shadow"
              >
                <div className="w-20 h-20 bg-gradient-to-br from-emerald-400 to-sky-400 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-white font-bold text-xl">
                    {member.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">
                  {member.name}
                </h3>
                <p className="text-emerald-600 font-medium mb-2">
                  {member.role}
                </p>
                <p className="text-sm text-gray-600">
                  {member.expertise}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                To democratize access to environmental forecasting by providing researchers, scientists, 
                and decision-makers with powerful tools to analyze satellite data and predict future trends.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                We believe that understanding our planet's patterns is crucial for sustainable development 
                and environmental protection.
              </p>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="grid grid-cols-2 gap-6"
            >
              {[
                { icon: <Globe className="w-8 h-8" />, title: 'Global Coverage', value: '100%' },
                { icon: <Database className="w-8 h-8" />, title: 'Data Sources', value: '3+' },
                { icon: <Brain className="w-8 h-8" />, title: 'ML Models', value: '3' },
                { icon: <TrendingUp className="w-8 h-8" />, title: 'Accuracy', value: '95%+' }
              ].map((stat, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="bg-white rounded-2xl p-6 text-center shadow-lg"
                >
                  <div className="text-emerald-600 mb-4 flex justify-center">
                    {stat.icon}
                  </div>
                  <div className="text-3xl font-bold text-gray-900 mb-2">{stat.value}</div>
                  <div className="text-gray-600">{stat.title}</div>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Technology Stack
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built with cutting-edge technologies for maximum performance and reliability.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'Data Sources',
                description: 'MODIS, MERRA-2, and ALOS PALSAR satellite data',
                icon: <Satellite className="w-8 h-8" />
              },
              {
                title: 'Machine Learning',
                description: 'ARIMA, Prophet, and LSTM models for predictions',
                icon: <Brain className="w-8 h-8" />
              },
              {
                title: 'Real-time Processing',
                description: 'FastAPI backend with async processing',
                icon: <Zap className="w-8 h-8" />
              }
            ].map((tech, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gradient-to-br from-emerald-50 to-sky-50 rounded-2xl p-8 text-center hover:shadow-lg transition-shadow"
              >
                <div className="text-emerald-600 mb-4 flex justify-center">
                  {tech.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {tech.title}
                </h3>
                <p className="text-gray-600">
                  {tech.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-emerald-600 to-sky-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Explore our datasets and start making predictions about our planet's future.
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-white text-emerald-600 px-8 py-4 rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300"
            >
              Explore Datasets
            </motion.button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};