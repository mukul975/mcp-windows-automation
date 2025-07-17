#!/usr/bin/env python3
"""
ML Predictive Engine for Windows Automation
Provides predictive automation capabilities including user behavior prediction,
system optimization, and smart automation recommendations.
"""

import os
import json
import pickle
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import psutil


@dataclass
class UserAction:
    """Represents a user action for ML training"""
    timestamp: datetime
    action_type: str
    application: str
    duration: float
    system_load: float
    memory_usage: float
    cpu_usage: float
    time_of_day: int
    day_of_week: int
    success: bool


@dataclass
class SystemMetrics:
    """System performance metrics"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_usage: float
    active_processes: int
    timestamp: datetime


class DataCollector:
    """Collects and stores user interaction and system data"""
    
    def __init__(self, data_file: str = "ml_data.json"):
        self.data_file = data_file
        self.actions: List[UserAction] = []
        self.metrics: List[SystemMetrics] = []
        self.load_data()
    
    def record_action(self, action_type: str, application: str, duration: float, success: bool = True):
        """Record a user action"""
        now = datetime.now()
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        action = UserAction(
            timestamp=now,
            action_type=action_type,
            application=application,
            duration=duration,
            system_load=cpu_percent,
            memory_usage=memory.percent,
            cpu_usage=cpu_percent,
            time_of_day=now.hour,
            day_of_week=now.weekday(),
            success=success
        )
        
        self.actions.append(action)
        self.save_data()
    
    def record_system_metrics(self):
        """Record current system metrics"""
        now = datetime.now()
        
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get network usage (simplified)
        network_usage = 0.0
        try:
            net_io = psutil.net_io_counters()
            network_usage = net_io.bytes_sent + net_io.bytes_recv
        except:
            pass
        
        metrics = SystemMetrics(
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=(disk.used / disk.total) * 100,
            network_usage=network_usage,
            active_processes=len(psutil.pids()),
            timestamp=now
        )
        
        self.metrics.append(metrics)
        self.save_data()
    
    def save_data(self):
        """Save collected data to file"""
        try:
            data = {
                'actions': [asdict(action) for action in self.actions],
                'metrics': [asdict(metric) for metric in self.metrics]
            }
            
            # Convert datetime objects to strings
            for action in data['actions']:
                action['timestamp'] = action['timestamp'].isoformat()
            
            for metric in data['metrics']:
                metric['timestamp'] = metric['timestamp'].isoformat()
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving data: {e}")
    
    def load_data(self):
        """Load data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Convert back to dataclass objects
                for action_data in data.get('actions', []):
                    action_data['timestamp'] = datetime.fromisoformat(action_data['timestamp'])
                    self.actions.append(UserAction(**action_data))
                
                for metric_data in data.get('metrics', []):
                    metric_data['timestamp'] = datetime.fromisoformat(metric_data['timestamp'])
                    self.metrics.append(SystemMetrics(**metric_data))
        
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            self.actions = []
            self.metrics = []


class UserBehaviorPredictor:
    """Predicts user behavior patterns"""
    
    def __init__(self, data_collector: DataCollector):
        self.data_collector = data_collector
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        self.model_file = "user_behavior_model.pkl"
        
    def train_user_behavior_model(self, user_data: List[Dict]) -> Dict[str, any]:
        """Train user behavior model with enhanced data processing"""
        try:
            if len(user_data) < 10:
                return {"error": f"Need at least 10 samples, have {len(user_data)}"}
            
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(user_data)
            
            # Prepare features
            feature_columns = ['hour', 'day_of_week', 'application_usage', 'click_count', 'window_switches', 'keystroke_count', 'idle_time']
            features = df[feature_columns].fillna(0).values
            
            # Use pattern as target if available, otherwise create synthetic targets
            if 'pattern' in df.columns:
                labels = df['pattern'].values
            else:
                # Create synthetic patterns based on usage intensity
                labels = []
                for _, row in df.iterrows():
                    activity_score = row['click_count'] + row['window_switches'] + (row['keystroke_count'] / 10)
                    if activity_score > 20:
                        labels.append('high_activity')
                    elif activity_score > 10:
                        labels.append('medium_activity')
                    else:
                        labels.append('low_activity')
            
            # Encode labels
            encoded_labels = self.label_encoder.fit_transform(labels)
            
            # Scale features
            scaled_features = self.scaler.fit_transform(features)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                scaled_features, encoded_labels, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate
            train_accuracy = accuracy_score(y_train, self.model.predict(X_train))
            test_accuracy = accuracy_score(y_test, self.model.predict(X_test))
            
            self.is_trained = True
            self.save_model()
            
            return {
                "train_accuracy": train_accuracy,
                "test_accuracy": test_accuracy,
                "samples_used": len(features),
                "feature_importance": dict(zip(feature_columns, self.model.feature_importances_))
            }
            
        except Exception as e:
            return {"error": f"Training failed: {str(e)}"}
    
    def predict_user_behavior(self, context: Dict) -> Dict[str, any]:
        """Predict user behavior based on context"""
        try:
            if not self.is_trained:
                self.load_model()
            
            if not self.is_trained:
                return {"error": "Model not trained"}
            
            # Prepare feature vector
            feature_vector = [
                context.get('hour', datetime.now().hour),
                context.get('day_of_week', datetime.now().weekday()),
                context.get('application_usage', 1),
                context.get('click_count', 5),
                context.get('window_switches', 2),
                context.get('keystroke_count', 50),
                context.get('idle_time', 30)
            ]
            
            scaled_features = self.scaler.transform([feature_vector])
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(scaled_features)[0]
            predicted_class = self.model.predict(scaled_features)[0]
            
            # Decode prediction
            predicted_behavior = self.label_encoder.inverse_transform([predicted_class])[0]
            confidence = max(probabilities)
            
            return {
                "predicted_behavior": predicted_behavior,
                "confidence": confidence,
                "all_probabilities": dict(zip(self.label_encoder.classes_, probabilities)),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def get_behavior_patterns(self) -> Dict[str, any]:
        """Analyze user behavior patterns"""
        try:
            if not self.data_collector.actions:
                return {"error": "No action data available"}
            
            # Convert to DataFrame
            actions_data = [asdict(action) for action in self.data_collector.actions]
            df = pd.DataFrame(actions_data)
            
            # Time-based patterns
            hourly_activity = df.groupby('time_of_day').size().to_dict()
            daily_activity = df.groupby('day_of_week').size().to_dict()
            
            # Application usage patterns
            app_usage = df['application'].value_counts().to_dict()
            
            # Action type patterns
            action_patterns = df['action_type'].value_counts().to_dict()
            
            # Success rate
            success_rate = df['success'].mean() if 'success' in df.columns else 1.0
            
            return {
                "hourly_activity": hourly_activity,
                "daily_activity": daily_activity,
                "app_usage": app_usage,
                "action_patterns": action_patterns,
                "success_rate": success_rate,
                "total_actions": len(df),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Pattern analysis failed: {str(e)}"}
    
    # Enhanced anomaly detection
    def detect_anomalies(self, threshold: float = 0.05) -> List[Dict[str, any]]:
        """Detect anomalous user behavior patterns"""
        try:
            if not self.is_trained or not self.data_collector.actions:
                return []
            
            anomalies = []
            recent_actions = self.data_collector.actions[-100:]  # Last 100 actions
            
            for action in recent_actions:
                # Create feature vector
                feature_vector = [
                    action.time_of_day,
                    action.day_of_week,
                    action.system_load,
                    action.memory_usage,
                    action.cpu_usage,
                    action.duration
                ]
                
                # Get prediction probability
                scaled_features = self.scaler.transform([feature_vector])
                probabilities = self.model.predict_proba(scaled_features)[0]
                
                # Check if probability is below threshold (anomaly)
                if max(probabilities) < threshold:
                    anomalies.append({
                        "timestamp": action.timestamp.isoformat(),
                        "action_type": action.action_type,
                        "application": action.application,
                        "anomaly_score": 1 - max(probabilities),
                        "reason": "Unusual behavior pattern detected"
                    })
            
            return sorted(anomalies, key=lambda x: x['anomaly_score'], reverse=True)
            
        except Exception as e:
            logging.error(f"Anomaly detection failed: {e}")
            return []
    
    def prepare_features(self, actions: List[UserAction]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for ML model"""
        if not actions:
            return np.array([]), np.array([])
        
        features = []
        labels = []
        
        for action in actions:
            feature_vector = [
                action.time_of_day,
                action.day_of_week,
                action.system_load,
                action.memory_usage,
                action.cpu_usage,
                action.duration
            ]
            features.append(feature_vector)
            labels.append(action.action_type)
        
        return np.array(features), np.array(labels)
    
    def train_model(self, min_samples: int = 50) -> Dict[str, float]:
        """Train the user behavior prediction model"""
        if len(self.data_collector.actions) < min_samples:
            return {"error": f"Need at least {min_samples} samples, have {len(self.data_collector.actions)}"}
        
        features, labels = self.prepare_features(self.data_collector.actions)
        
        if len(features) == 0:
            return {"error": "No features available for training"}
        
        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(labels)
        
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            scaled_features, encoded_labels, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_accuracy = accuracy_score(y_train, self.model.predict(X_train))
        test_accuracy = accuracy_score(y_test, self.model.predict(X_test))
        
        self.is_trained = True
        self.save_model()
        
        return {
            "train_accuracy": train_accuracy,
            "test_accuracy": test_accuracy,
            "samples_used": len(features)
        }
    
    def predict_next_action(self, current_context: Dict) -> Dict[str, any]:
        """Predict the most likely next action"""
        if not self.is_trained:
            self.load_model()
        
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        try:
            # Get current system metrics
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            now = datetime.now()
            
            feature_vector = [
                now.hour,
                now.weekday(),
                cpu_percent,
                memory.percent,
                cpu_percent,
                current_context.get('duration', 0)
            ]
            
            scaled_features = self.scaler.transform([feature_vector])
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(scaled_features)[0]
            predicted_class = self.model.predict(scaled_features)[0]
            
            # Decode prediction
            predicted_action = self.label_encoder.inverse_transform([predicted_class])[0]
            confidence = max(probabilities)
            
            return {
                "predicted_action": predicted_action,
                "confidence": confidence,
                "timestamp": now.isoformat()
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def save_model(self):
        """Save trained model"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoder': self.label_encoder,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, self.model_file)
        except Exception as e:
            logging.error(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model"""
        try:
            if os.path.exists(self.model_file):
                model_data = joblib.load(self.model_file)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.label_encoder = model_data['label_encoder']
                self.is_trained = model_data['is_trained']
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            self.is_trained = False


class SystemOptimizer:
    """Optimizes system performance using ML predictions"""
    
    def __init__(self, data_collector: DataCollector):
        self.data_collector = data_collector
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_file = "system_optimizer_model.pkl"
    
    def prepare_features(self, metrics: List[SystemMetrics]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features for system optimization model"""
        if not metrics:
            return np.array([]), np.array([])
        
        features = []
        targets = []
        
        for i, metric in enumerate(metrics[:-1]):  # Skip last one for target
            next_metric = metrics[i + 1]
            
            feature_vector = [
                metric.cpu_usage,
                metric.memory_usage,
                metric.disk_usage,
                metric.active_processes,
                metric.timestamp.hour,
                metric.timestamp.weekday()
            ]
            
            # Target: next CPU usage (as optimization target)
            target = next_metric.cpu_usage
            
            features.append(feature_vector)
            targets.append(target)
        
        return np.array(features), np.array(targets)
    
    def train_model(self, min_samples: int = 100) -> Dict[str, float]:
        """Train system optimization model"""
        if len(self.data_collector.metrics) < min_samples:
            return {"error": f"Need at least {min_samples} samples, have {len(self.data_collector.metrics)}"}
        
        features, targets = self.prepare_features(self.data_collector.metrics)
        
        if len(features) == 0:
            return {"error": "No features available for training"}
        
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            scaled_features, targets, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_mse = mean_squared_error(y_train, self.model.predict(X_train))
        test_mse = mean_squared_error(y_test, self.model.predict(X_test))
        
        self.is_trained = True
        self.save_model()
        
        return {
            "train_mse": train_mse,
            "test_mse": test_mse,
            "samples_used": len(features)
        }
    
    def train_system_load_model(self, min_samples: int = 100) -> Dict[str, float]:
        """Train system load model"""
        if len(self.data_collector.metrics) < min_samples:
            return {"error": f"Need at least {min_samples} samples, have {len(self.data_collector.metrics)}"}
        
        features, targets = self.prepare_features(self.data_collector.metrics)
        
        if len(features) == 0:
            return {"error": "No features available for training"}
        
        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            scaled_features, targets, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_mse = mean_squared_error(y_train, self.model.predict(X_train))
        test_mse = mean_squared_error(y_test, self.model.predict(X_test))
        
        self.is_trained = True
        self.save_model()
        
        return {
            "train_mse": train_mse,
            "test_mse": test_mse,
            "samples_used": len(features)
        }

    def predict_system_load(self, current_system_metrics=None) -> Dict[str, any]:
        """Predict future system load"""
        if not self.is_trained:
            self.load_model()
        
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        try:
            # Use provided metrics or get current system metrics
            if current_system_metrics:
                cpu_usage = current_system_metrics['cpu_usage']
                memory = current_system_metrics['memory']
                disk = current_system_metrics['disk']
            else:
                cpu_usage = psutil.cpu_percent()
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
            now = datetime.now()
            
            feature_vector = [
                cpu_usage,
                memory.percent,
                (disk.used / disk.total) * 100,
                len(psutil.pids()),
                now.hour,
                now.weekday()
            ]
            
            scaled_features = self.scaler.transform([feature_vector])
            predicted_load = self.model.predict(scaled_features)[0]
            
            return {
                "predicted_cpu_load": predicted_load,
                "current_cpu_load": cpu_usage,
                "timestamp": now.isoformat()
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def save_model(self):
        """Save trained model"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, self.model_file)
        except Exception as e:
            logging.error(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model"""
        try:
            if os.path.exists(self.model_file):
                model_data = joblib.load(self.model_file)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.is_trained = model_data['is_trained']
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            self.is_trained = False


class AutomationRecommendationEngine:
    """Provides smart automation recommendations"""
    
    def __init__(self, data_collector: DataCollector, behavior_predictor: UserBehaviorPredictor):
        self.data_collector = data_collector
        self.behavior_predictor = behavior_predictor
    
    def get_recommendations(self) -> List[Dict[str, any]]:
        """Get automation recommendations based on user behavior"""
        recommendations = []
        
        # Analyze user patterns
        if len(self.data_collector.actions) < 10:
            return [{"recommendation": "Collect more usage data for better recommendations"}]
        
        # Common patterns analysis
        action_frequency = {}
        for action in self.data_collector.actions:
            key = f"{action.action_type}_{action.application}"
            action_frequency[key] = action_frequency.get(key, 0) + 1
        
        # Sort by frequency
        sorted_actions = sorted(action_frequency.items(), key=lambda x: x[1], reverse=True)
        
        # Generate recommendations
        for action_key, frequency in sorted_actions[:5]:
            action_type, application = action_key.split('_', 1)
            
            if frequency > 5:  # Frequent action
                recommendations.append({
                    "type": "automation",
                    "action": action_type,
                    "application": application,
                    "frequency": frequency,
                    "recommendation": f"Consider automating {action_type} in {application} (used {frequency} times)"
                })
        
        # Time-based recommendations
        time_patterns = {}
        for action in self.data_collector.actions:
            hour = action.time_of_day
            if hour not in time_patterns:
                time_patterns[hour] = []
            time_patterns[hour].append(action.action_type)
        
        for hour, actions in time_patterns.items():
            if len(actions) > 3:  # Active hour
                most_common = max(set(actions), key=actions.count)
                recommendations.append({
                    "type": "schedule",
                    "hour": hour,
                    "action": most_common,
                    "recommendation": f"Schedule {most_common} automation at {hour}:00 (frequently used)"
                })
        
        return recommendations


# Initialize global instances
data_collector = DataCollector()
behavior_predictor = UserBehaviorPredictor(data_collector)
system_optimizer = SystemOptimizer(data_collector)
recommendation_engine = AutomationRecommendationEngine(data_collector, behavior_predictor)


def get_ml_engine():
    """Get ML engine instances"""
    return {
        'data_collector': data_collector,
        'behavior_predictor': behavior_predictor,
        'system_optimizer': system_optimizer,
        'recommendation_engine': recommendation_engine
    }
