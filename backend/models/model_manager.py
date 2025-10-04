"""
Model management module for persistent storage and loading of trained models.

This module handles saving, loading, and managing trained machine learning models
for time-series forecasting in the BloomTracker system.
"""

import os
import json
import pickle
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manages persistent storage and loading of trained machine learning models.
    
    This class handles saving models to disk, loading existing models,
    and managing model metadata for the BloomTracker prediction system.
    """
    
    def __init__(self, models_dir: str = "models/saved_models"):
        """
        Initialize the model manager.
        
        Args:
            models_dir (str): Directory to store saved models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.models_dir / "model_metadata.json"
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, Any]:
        """
        Load model metadata from disk.
        
        Returns:
            Dict containing model metadata
        """
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            logger.warning(f"Could not load model metadata: {str(e)}")
            return {}
    
    def _save_metadata(self):
        """Save model metadata to disk."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving model metadata: {str(e)}")
    
    def get_model_path(self, dataset: str, model_type: str) -> Path:
        """
        Get the file path for a specific model.
        
        Args:
            dataset (str): Dataset name (modis, merra, alos)
            model_type (str): Model type (arima, prophet, lstm)
            
        Returns:
            Path: File path for the model
        """
        return self.models_dir / f"{dataset}_{model_type}.pkl"
    
    def model_exists(self, dataset: str, model_type: str) -> bool:
        """
        Check if a model exists for the given dataset and type.
        
        Args:
            dataset (str): Dataset name
            model_type (str): Model type
            
        Returns:
            bool: True if model exists
        """
        model_path = self.get_model_path(dataset, model_type)
        return model_path.exists()
    
    def get_model_info(self, dataset: str, model_type: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a saved model.
        
        Args:
            dataset (str): Dataset name
            model_type (str): Model type
            
        Returns:
            Dict containing model information or None if not found
        """
        model_key = f"{dataset}_{model_type}"
        return self.metadata.get(model_key)
    
    def is_model_fresh(self, dataset: str, model_type: str, max_age_days: int = 7) -> bool:
        """
        Check if a model is fresh (recently trained).
        
        Args:
            dataset (str): Dataset name
            model_type (str): Model type
            max_age_days (int): Maximum age in days
            
        Returns:
            bool: True if model is fresh
        """
        model_info = self.get_model_info(dataset, model_type)
        if not model_info:
            return False
        
        try:
            last_updated = datetime.fromisoformat(model_info.get('last_updated', ''))
            age = datetime.now() - last_updated
            return age.days <= max_age_days
        except:
            return False
    
    def save_model(self, dataset: str, model_type: str, model: Any, 
                   training_data: pd.DataFrame, metadata: Dict[str, Any]) -> bool:
        """
        Save a trained model to disk.
        
        Args:
            dataset (str): Dataset name
            model_type (str): Model type
            model: Trained model object
            training_data (pd.DataFrame): Training data used
            metadata (Dict): Additional model metadata
            
        Returns:
            bool: True if saved successfully
        """
        try:
            model_path = self.get_model_path(dataset, model_type)
            
            # Prepare model data for saving
            model_data = {
                'model': model,
                'training_data': training_data,
                'metadata': metadata,
                'dataset': dataset,
                'model_type': model_type,
                'saved_at': datetime.now().isoformat()
            }
            
            # Save model
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            # Update metadata
            model_key = f"{dataset}_{model_type}"
            self.metadata[model_key] = {
                'dataset': dataset,
                'model_type': model_type,
                'last_updated': datetime.now().isoformat(),
                'training_samples': len(training_data),
                'file_size': model_path.stat().st_size,
                'metadata': metadata
            }
            
            self._save_metadata()
            logger.info(f"Model saved: {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model {dataset}_{model_type}: {str(e)}")
            return False
    
    def load_model(self, dataset: str, model_type: str) -> Optional[Tuple[Any, pd.DataFrame, Dict[str, Any]]]:
        """
        Load a saved model from disk.
        
        Args:
            dataset (str): Dataset name
            model_type (str): Model type
            
        Returns:
            Tuple of (model, training_data, metadata) or None if not found
        """
        try:
            model_path = self.get_model_path(dataset, model_type)
            
            if not model_path.exists():
                logger.warning(f"Model not found: {model_path}")
                return None
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            logger.info(f"Model loaded: {model_path}")
            return (
                model_data['model'],
                model_data['training_data'],
                model_data['metadata']
            )
            
        except Exception as e:
            logger.error(f"Error loading model {dataset}_{model_type}: {str(e)}")
            return None
    
    def delete_model(self, dataset: str, model_type: str) -> bool:
        """
        Delete a saved model.
        
        Args:
            dataset (str): Dataset name
            model_type (str): Model type
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            model_path = self.get_model_path(dataset, model_type)
            
            if model_path.exists():
                model_path.unlink()
            
            # Remove from metadata
            model_key = f"{dataset}_{model_type}"
            if model_key in self.metadata:
                del self.metadata[model_key]
                self._save_metadata()
            
            logger.info(f"Model deleted: {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting model {dataset}_{model_type}: {str(e)}")
            return False
    
    def list_models(self) -> Dict[str, Any]:
        """
        List all saved models.
        
        Returns:
            Dict containing information about all saved models
        """
        models_info = {}
        
        for model_key, model_info in self.metadata.items():
            dataset, model_type = model_key.split('_', 1)
            
            if dataset not in models_info:
                models_info[dataset] = {}
            
            models_info[dataset][model_type] = {
                'last_updated': model_info.get('last_updated'),
                'training_samples': model_info.get('training_samples', 0),
                'file_size': model_info.get('file_size', 0),
                'exists': self.model_exists(dataset, model_type)
            }
        
        return models_info
    
    def cleanup_old_models(self, max_age_days: int = 30) -> int:
        """
        Clean up old models that are no longer needed.
        
        Args:
            max_age_days (int): Maximum age in days
            
        Returns:
            int: Number of models cleaned up
        """
        cleaned_count = 0
        
        try:
            for model_key, model_info in list(self.metadata.items()):
                last_updated = datetime.fromisoformat(model_info.get('last_updated', ''))
                age = datetime.now() - last_updated
                
                if age.days > max_age_days:
                    dataset, model_type = model_key.split('_', 1)
                    if self.delete_model(dataset, model_type):
                        cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} old models")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old models: {str(e)}")
            return 0
    
    def get_model_stats(self) -> Dict[str, Any]:
        """
        Get statistics about saved models.
        
        Returns:
            Dict containing model statistics
        """
        total_models = len(self.metadata)
        total_size = sum(info.get('file_size', 0) for info in self.metadata.values())
        
        datasets = set()
        model_types = set()
        
        for model_key in self.metadata.keys():
            dataset, model_type = model_key.split('_', 1)
            datasets.add(dataset)
            model_types.add(model_type)
        
        return {
            'total_models': total_models,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'datasets': list(datasets),
            'model_types': list(model_types),
            'models_by_dataset': {
                dataset: len([k for k in self.metadata.keys() if k.startswith(f"{dataset}_")])
                for dataset in datasets
            }
        }
