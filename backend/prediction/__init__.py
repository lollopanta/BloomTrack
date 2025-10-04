"""
Prediction module for BloomTracker backend.

This module provides time-series forecasting capabilities for geospatial data
using various machine learning models including ARIMA, Prophet, and LSTM.
"""

from .predictor import PredictiveModel, TimeSeriesPredictor

__all__ = ['PredictiveModel', 'TimeSeriesPredictor']
