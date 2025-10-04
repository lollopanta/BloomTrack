import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from pathlib import Path

from app.models.plant_models import PlantBloomEvent, BloomIntensity, VegetationType, Season

class MLBloomPredictor:
    """Machine Learning models for bloom prediction and analysis"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.model_dir = Path("models")
        self.model_dir.mkdir(exist_ok=True)
    
    def prepare_training_data(self, events: List[PlantBloomEvent]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data from bloom events"""
        data = []
        targets = []
        
        for event in events:
            # Feature engineering
            features = [
                event.latitude,
                event.longitude,
                event.detection_date.month,
                event.detection_date.day,
                event.detection_date.timetuple().tm_yday,  # day of year
                event.confidence,
                self._encode_vegetation_type(event.vegetation_type),
                self._encode_season(event.season),
                self._encode_intensity(event.intensity),
                event.area_coverage,
                event.duration_days,
                event.conservation_priority or 0
            ]
            
            # Add spectral features if available
            if hasattr(event, 'spectral_bands') and event.spectral_bands:
                features.extend([
                    event.spectral_bands.get('NDVI', 0),
                    event.spectral_bands.get('EVI', 0),
                    event.spectral_bands.get('SAVI', 0)
                ])
            else:
                features.extend([0, 0, 0])  # Default values
            
            data.append(features)
            
            # Target: bloom intensity as numeric value
            intensity_mapping = {'low': 1, 'medium': 2, 'high': 3}
            targets.append(intensity_mapping.get(event.intensity.value, 2))
        
        return np.array(data), np.array(targets)
    
    def _encode_vegetation_type(self, vegetation_type: VegetationType) -> int:
        """Encode vegetation type to numeric"""
        mapping = {
            VegetationType.FOREST: 1,
            VegetationType.GRASSLAND: 2,
            VegetationType.AGRICULTURAL: 3,
            VegetationType.DESERT: 4,
            VegetationType.WETLAND: 5,
            VegetationType.SHRUBLAND: 6
        }
        return mapping.get(vegetation_type, 0)
    
    def _encode_season(self, season: Season) -> int:
        """Encode season to numeric"""
        mapping = {
            Season.SPRING: 1,
            Season.SUMMER: 2,
            Season.AUTUMN: 3,
            Season.WINTER: 4
        }
        return mapping.get(season, 0)
    
    def _encode_intensity(self, intensity: BloomIntensity) -> int:
        """Encode intensity to numeric"""
        mapping = {
            BloomIntensity.LOW: 1,
            BloomIntensity.MEDIUM: 2,
            BloomIntensity.HIGH: 3
        }
        return mapping.get(intensity, 2)
    
    def train_bloom_intensity_model(self, events: List[PlantBloomEvent]) -> Dict[str, Any]:
        """Train model to predict bloom intensity"""
        X, y = self.prepare_training_data(events)
        
        if len(X) < 10:  # Need minimum data for training
            return {"error": "Insufficient data for training (need at least 10 events)"}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train multiple models
        models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'linear_regression': LinearRegression()
        }
        
        results = {}
        best_model = None
        best_score = -np.inf
        
        for name, model in models.items():
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            
            results[name] = {
                'mse': mse,
                'r2': r2,
                'mae': mae,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            # Track best model
            if r2 > best_score:
                best_score = r2
                best_model = model
        
        # Save best model
        if best_model:
            model_path = self.model_dir / "bloom_intensity_model.pkl"
            joblib.dump(best_model, model_path)
            self.models['bloom_intensity'] = best_model
            self.scalers['bloom_intensity'] = scaler
        
        return {
            'model_results': results,
            'best_model': max(results.keys(), key=lambda k: results[k]['r2']),
            'best_r2': best_score,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict_bloom_intensity(self, latitude: float, longitude: float, 
                              date: datetime, vegetation_type: str,
                              area_coverage: float = 100.0) -> Dict[str, Any]:
        """Predict bloom intensity for given parameters"""
        if 'bloom_intensity' not in self.models:
            return {"error": "Model not trained. Please train the model first."}
        
        # Prepare input features
        features = [
            latitude,
            longitude,
            date.month,
            date.day,
            date.timetuple().tm_yday,
            75.0,  # Default confidence
            self._encode_vegetation_type(VegetationType(vegetation_type)),
            self._get_season_from_date(date),
            2,  # Default intensity
            area_coverage,
            30,  # Default duration
            3   # Default priority
        ]
        
        # Add default spectral values
        features.extend([0.5, 0.4, 0.45])  # Default NDVI, EVI, SAVI
        
        # Scale features
        X = np.array(features).reshape(1, -1)
        X_scaled = self.scalers['bloom_intensity'].transform(X)
        
        # Make prediction
        prediction = self.models['bloom_intensity'].predict(X_scaled)[0]
        
        # Convert prediction to intensity category
        if prediction < 1.5:
            intensity = 'low'
        elif prediction < 2.5:
            intensity = 'medium'
        else:
            intensity = 'high'
        
        return {
            'predicted_intensity': intensity,
            'confidence_score': prediction,
            'probability_distribution': {
                'low': max(0, 1 - abs(prediction - 1)),
                'medium': max(0, 1 - abs(prediction - 2)),
                'high': max(0, 1 - abs(prediction - 3))
            }
        }
    
    def _get_season_from_date(self, date: datetime) -> int:
        """Determine season from date"""
        month = date.month
        if month in [12, 1, 2]:
            return 4  # Winter
        elif month in [3, 4, 5]:
            return 1  # Spring
        elif month in [6, 7, 8]:
            return 2  # Summer
        else:
            return 3  # Autumn
    
    def train_bloom_timing_model(self, events: List[PlantBloomEvent]) -> Dict[str, Any]:
        """Train model to predict bloom timing"""
        # Prepare timing data
        timing_data = []
        for event in events:
            timing_data.append({
                'latitude': event.latitude,
                'longitude': event.longitude,
                'vegetation_type': event.vegetation_type.value,
                'day_of_year': event.detection_date.timetuple().tm_yday,
                'year': event.detection_date.year
            })
        
        df = pd.DataFrame(timing_data)
        
        if len(df) < 10:
            return {"error": "Insufficient data for timing model"}
        
        # Encode categorical variables
        le_vegetation = LabelEncoder()
        df['vegetation_encoded'] = le_vegetation.fit_transform(df['vegetation_type'])
        
        # Features and target
        X = df[['latitude', 'longitude', 'vegetation_encoded']].values
        y = df['day_of_year'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Save model
        model_path = self.model_dir / "bloom_timing_model.pkl"
        joblib.dump(model, model_path)
        self.models['bloom_timing'] = model
        self.scalers['bloom_timing'] = scaler
        self.label_encoders['vegetation'] = le_vegetation
        
        return {
            'mse': mse,
            'r2': r2,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict_bloom_timing(self, latitude: float, longitude: float, 
                           vegetation_type: str, year: int = None) -> Dict[str, Any]:
        """Predict bloom timing for given location and vegetation type"""
        if 'bloom_timing' not in self.models:
            return {"error": "Timing model not trained"}
        
        if year is None:
            year = datetime.now().year
        
        # Prepare features
        vegetation_encoded = self.label_encoders['vegetation'].transform([vegetation_type])[0]
        X = np.array([[latitude, longitude, vegetation_encoded]])
        X_scaled = self.scalers['bloom_timing'].transform(X)
        
        # Make prediction
        day_of_year = self.models['bloom_timing'].predict(X_scaled)[0]
        
        # Convert to date
        bloom_date = datetime(year, 1, 1) + timedelta(days=int(day_of_year) - 1)
        
        return {
            'predicted_day_of_year': int(day_of_year),
            'predicted_date': bloom_date.isoformat(),
            'confidence': 'medium',  # Could be improved with uncertainty quantification
            'season': self._get_season_from_date(bloom_date)
        }
    
    def analyze_bloom_anomalies(self, events: List[PlantBloomEvent]) -> Dict[str, Any]:
        """Analyze anomalies in bloom patterns using ML"""
        if len(events) < 20:
            return {"error": "Insufficient data for anomaly analysis"}
        
        # Prepare data
        X, y = self.prepare_training_data(events)
        
        # Train isolation forest for anomaly detection
        from sklearn.ensemble import IsolationForest
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(X)
        
        # Identify anomalies
        anomalies = []
        for i, (event, is_anomaly) in enumerate(zip(events, anomaly_labels)):
            if is_anomaly == -1:  # Anomaly detected
                anomalies.append({
                    'event_id': event.id,
                    'location': event.location,
                    'date': event.detection_date.isoformat(),
                    'intensity': event.intensity.value,
                    'anomaly_score': iso_forest.decision_function([X[i]])[0],
                    'reason': self._analyze_anomaly_reason(event, events)
                })
        
        return {
            'total_events': len(events),
            'anomalies_detected': len(anomalies),
            'anomaly_rate': len(anomalies) / len(events),
            'anomalies': anomalies
        }
    
    def _analyze_anomaly_reason(self, event: PlantBloomEvent, all_events: List[PlantBloomEvent]) -> str:
        """Analyze why an event is considered anomalous"""
        reasons = []
        
        # Check for unusual timing
        same_region_events = [e for e in all_events if e.region == event.region]
        if same_region_events:
            avg_month = np.mean([e.detection_date.month for e in same_region_events])
            if abs(event.detection_date.month - avg_month) > 2:
                reasons.append("unusual_timing")
        
        # Check for unusual intensity
        if event.intensity == BloomIntensity.HIGH and event.vegetation_type == VegetationType.DESERT:
            reasons.append("high_intensity_desert")
        
        # Check for unusual area
        if event.area_coverage > 5000:  # Very large area
            reasons.append("unusually_large_area")
        
        return "; ".join(reasons) if reasons else "statistical_outlier"
    
    def generate_bloom_forecast(self, events: List[PlantBloomEvent], 
                               forecast_months: int = 6) -> Dict[str, Any]:
        """Generate bloom forecast for upcoming months"""
        if len(events) < 30:
            return {"error": "Insufficient historical data for forecasting"}
        
        # Prepare time series data
        df = pd.DataFrame([{
            'date': event.detection_date,
            'latitude': event.latitude,
            'longitude': event.longitude,
            'intensity': self._encode_intensity(event.intensity),
            'area': event.area_coverage
        } for event in events])
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date').sort_index()
        
        # Simple trend analysis
        monthly_counts = df.resample('M').size()
        
        # Generate forecast (simplified)
        last_month = monthly_counts.index[-1]
        forecast_dates = pd.date_range(
            start=last_month + pd.DateOffset(months=1),
            periods=forecast_months,
            freq='M'
        )
        
        # Simple linear trend
        if len(monthly_counts) > 3:
            trend = np.polyfit(range(len(monthly_counts)), monthly_counts.values, 1)[0]
            base_forecast = monthly_counts.iloc[-1] + trend
        else:
            base_forecast = monthly_counts.mean()
        
        forecast = []
        for i, date in enumerate(forecast_dates):
            # Add seasonal variation
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)
            predicted_count = max(0, base_forecast * seasonal_factor)
            
            forecast.append({
                'date': date.isoformat(),
                'predicted_events': int(predicted_count),
                'confidence': 'medium',
                'season': self._get_season_from_date(date)
            })
        
        return {
            'forecast_period': f"{forecast_months} months",
            'historical_avg': monthly_counts.mean(),
            'trend': 'increasing' if trend > 0 else 'decreasing' if trend < 0 else 'stable',
            'forecast': forecast
        }

