import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Menu, X, Satellite, Home, Info, Database, Leaf } from 'lucide-react';
import { cn } from '../utils';

const NavItem: React.FC<{ href: string; icon: React.ReactNode; children: React.ReactNode; isActive: boolean }> = ({
  href,
  icon,
  children,
  isActive
}) => (
  <Link
    to={href}
    className={cn(
      'flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200',
      isActive
        ? 'bg-primary-100 text-primary-700'
        : 'text-gray-600 hover:text-primary-600 hover:bg-primary-50'
    )}
  >
    {icon}
    <span>{children}</span>
  </Link>
);

export const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { href: '/', icon: <Home className="w-4 h-4" />, label: 'Home' },
    { href: '/about', icon: <Info className="w-4 h-4" />, label: 'About' },
    { href: '/datasets', icon: <Database className="w-4 h-4" />, label: 'Datasets' },
    { href: '/dati-simulati', icon: <Leaf className="w-4 h-4" />, label: 'Plant Simulator' },
  ];

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-white shadow-lg border-b border-gray-200"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <motion.div
              whileHover={{ rotate: 360 }}
              transition={{ duration: 0.5 }}
              className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-primary-500 to-sky-500 rounded-lg"
            >
              <Satellite className="w-6 h-6 text-white" />
            </motion.div>
            <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-sky-600 bg-clip-text text-transparent">
              BloomTracker
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <NavItem
                key={item.href}
                href={item.href}
                icon={item.icon}
                isActive={location.pathname === item.href}
              >
                {item.label}
              </NavItem>
            ))}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-primary-600 hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            >
              {isOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden"
          >
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-200">
              {navItems.map((item) => (
                <NavItem
                  key={item.href}
                  href={item.href}
                  icon={item.icon}
                  isActive={location.pathname === item.href}
                >
                  {item.label}
                </NavItem>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </motion.nav>
  );
};
