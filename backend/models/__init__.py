"""
Model management module for BloomTracker backend.

This module handles persistent storage and loading of trained machine learning models
for time-series forecasting of geospatial data.
"""

from .model_manager import ModelManager

__all__ = ['ModelManager']
