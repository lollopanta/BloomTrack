import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Github, Twitter, Linkedin } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and Description */}
          <div className="col-span-1 md:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h3 className="text-2xl font-bold text-emerald-400 mb-4">BloomTracker</h3>
              <p className="text-gray-300 mb-6 max-w-md">
                Forecasting the future of Earth from space using satellite data and machine learning. 
                Developed for NASA Space Apps Challenge 2025 by the CyberHive team.
              </p>
              <div className="flex space-x-4">
                <motion.a
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  href="https://github.com"
                  className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-emerald-600 transition-colors"
                >
                  <Github className="w-5 h-5" />
                </motion.a>
              </div>
            </motion.div>
          </div>

          {/* Quick Links */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              viewport={{ once: true }}
            >
              <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2">
                <li><a href="/" className="text-gray-300 hover:text-emerald-400 transition-colors">Home</a></li>
                <li><a href="/dataset/modis" className="text-gray-300 hover:text-emerald-400 transition-colors">MODIS Data</a></li>
                <li><a href="/dataset/merra" className="text-gray-300 hover:text-emerald-400 transition-colors">MERRA-2 Data</a></li>
                <li><a href="/dataset/alos" className="text-gray-300 hover:text-emerald-400 transition-colors">ALOS Data</a></li>
                <li><a href="/about" className="text-gray-300 hover:text-emerald-400 transition-colors">About</a></li>
              </ul>
            </motion.div>
          </div>

          {/* Resources */}
          <div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <h4 className="text-lg font-semibold mb-4">Resources</h4>
              <ul className="space-y-2">
                <li><a href="https://modis.gsfc.nasa.gov" className="text-gray-300 hover:text-emerald-400 transition-colors">MODIS</a></li>
                <li><a href="https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2" className="text-gray-300 hover:text-emerald-400 transition-colors">MERRA-2</a></li>
                <li><a href="https://www.eorc.jaxa.jp/ALOS/en/about/palsar.htm" className="text-gray-300 hover:text-emerald-400 transition-colors">ALOS PALSAR</a></li>
                <li><a href="https://www.spaceappschallenge.org" className="text-gray-300 hover:text-emerald-400 transition-colors">NASA Space Apps</a></li>
              </ul>
            </motion.div>
          </div>
        </div>

        {/* Bottom Bar */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
          className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center"
        >
          <div className="flex items-center space-x-2 text-gray-400 mb-4 md:mb-0">
            <span>Made with</span>
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              <Heart className="w-4 h-4 text-red-500" />
            </motion.div>
            <span>by CyberHive for NASA Space Apps 2025</span>
          </div>
          <div className="text-gray-400 text-sm">
            © 2025 BloomTracker. All rights reserved.
          </div>
        </motion.div>
      </div>
    </footer>
  );
};
