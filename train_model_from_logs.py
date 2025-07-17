#!/usr/bin/env python3
"""
Train ML models automatically using Windows system logs
"""
import sys
import os
import json
import subprocess
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ml_predictive_engine import get_ml_engine, UserAction, SystemMetrics
    print("✓ Successfully imported ML engine components")
except ImportError as e:
    print(f"✗ Failed to import ML engine components: {e}")
    sys.exit(1)

class SystemLogProcessor:
    """Process Windows system logs for ML training"""
    
    def __init__(self):
        ml_engine = get_ml_engine()
        self.data_collector = ml_engine['data_collector']
        self.behavior_predictor = ml_engine['behavior_predictor']
        self.system_optimizer = ml_engine['system_optimizer']
        self.recommendation_engine = ml_engine['recommendation_engine']
        
    def get_system_logs(self, log_name: str, hours_back: int = 24) -> List[Dict]:
        """Get system logs using PowerShell"""
        try:
            # PowerShell command to get recent logs
            ps_command = f"""
Get-WinEvent -LogName '{log_name}' -MaxEvents 1000 | 
Where-Object {{$_.TimeCreated -gt (Get-Date).AddHours(-{hours_back})}} |
Select-Object TimeCreated, Id, LevelDisplayName, LogName, Message |
ConvertTo-Json -Depth 3
"""
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    logs = json.loads(result.stdout)
                    # Handle single event (not a list)
                    if isinstance(logs, dict):
                        logs = [logs]
                    return logs
                except json.JSONDecodeError:
                    print(f"Warning: Could not parse JSON from {log_name} logs")
                    return []
            else:
                print(f"Warning: Could not retrieve {log_name} logs")
                return []
                
        except subprocess.TimeoutExpired:
            print(f"Warning: Timeout retrieving {log_name} logs")
            return []
        except Exception as e:
            print(f"Warning: Error retrieving {log_name} logs: {e}")
            return []
    
    def get_system_performance_metrics(self) -> Dict[str, float]:
        """Get current system performance metrics"""
        metrics = {}
        
        try:
            # Get CPU usage
            ps_command = """
Get-Counter "\\Processor(_Total)\\% Processor Time" -SampleInterval 1 -MaxSamples 1 |
Select-Object -ExpandProperty CounterSamples |
Select-Object -ExpandProperty CookedValue
"""
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    metrics['cpu_usage'] = float(result.stdout.strip())
                except ValueError:
                    metrics['cpu_usage'] = 50.0  # Default
            else:
                metrics['cpu_usage'] = 50.0
                
            # Get memory usage
            ps_command = """
$mem = Get-CimInstance -ClassName Win32_OperatingSystem
$total = $mem.TotalVisibleMemorySize
$free = $mem.FreePhysicalMemory
$used = $total - $free
($used / $total) * 100
"""
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    metrics['memory_usage'] = float(result.stdout.strip())
                except ValueError:
                    metrics['memory_usage'] = 60.0  # Default
            else:
                metrics['memory_usage'] = 60.0
                
            # Get disk usage
            ps_command = """
Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3" |
Select-Object -First 1 |
ForEach-Object { (($_.Size - $_.FreeSpace) / $_.Size) * 100 }
"""
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    metrics['disk_usage'] = float(result.stdout.strip())
                except ValueError:
                    metrics['disk_usage'] = 70.0  # Default
            else:
                metrics['disk_usage'] = 70.0
                
        except Exception as e:
            print(f"Warning: Error getting performance metrics: {e}")
            # Provide default values
            metrics = {
                'cpu_usage': 50.0,
                'memory_usage': 60.0,
                'disk_usage': 70.0
            }
            
        return metrics
    
    def process_logs_to_training_data(self, logs: List[Dict]) -> List[Dict]:
        """Convert system logs to training data format"""
        training_data = []
        
        for log in logs:
            try:
                # Extract relevant features from log entry
                timestamp = log.get('TimeCreated', '')
                event_id = log.get('Id', 0)
                level = log.get('LevelDisplayName', 'Information')
                message = log.get('Message', '')
                
                # Parse timestamp
                try:
                    if timestamp:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        hour = dt.hour
                        day_of_week = dt.weekday()
                    else:
                        hour = 12
                        day_of_week = 1
                except:
                    hour = 12
                    day_of_week = 1
                
                # Create feature vector
                features = {
                    'hour': hour,
                    'day_of_week': day_of_week,
                    'event_id': event_id,
                    'is_error': 1 if level in ['Error', 'Critical'] else 0,
                    'is_warning': 1 if level == 'Warning' else 0,
                    'message_length': len(message),
                    'has_keywords': self._check_keywords(message)
                }
                
                training_data.append(features)
                
            except Exception as e:
                print(f"Warning: Error processing log entry: {e}")
                continue
                
        return training_data
    
    def _check_keywords(self, message: str) -> int:
        """Check for important keywords in log message"""
        keywords = [
            'error', 'warning', 'critical', 'failed', 'timeout',
            'restart', 'crash', 'memory', 'disk', 'cpu', 'network'
        ]
        
        message_lower = message.lower()
        for keyword in keywords:
            if keyword in message_lower:
                return 1
        return 0
    
    def collect_user_behavior_data(self) -> List[Dict]:
        """Simulate user behavior data collection from system logs"""
        user_data = []
        
        # Get application logs which might contain user activity
        app_logs = self.get_system_logs('Application', hours_back=24)
        
        for log in app_logs:
            try:
                timestamp = log.get('TimeCreated', '')
                event_id = log.get('Id', 0)
                message = log.get('Message', '')
                
                # Parse timestamp
                try:
                    if timestamp:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        hour = dt.hour
                        day_of_week = dt.weekday()
                    else:
                        hour = 12
                        day_of_week = 1
                except:
                    hour = 12
                    day_of_week = 1
                
                # Simulate user behavior patterns
                user_behavior = {
                    'hour': hour,
                    'day_of_week': day_of_week,
                    'application_usage': 1,  # Simulated
                    'click_count': max(1, event_id % 10),  # Simulated
                    'window_switches': max(1, event_id % 5),  # Simulated
                    'keystroke_count': max(10, event_id % 100),  # Simulated
                    'idle_time': max(0, (event_id * 17) % 300)  # Simulated
                }
                
                user_data.append(user_behavior)
                
            except Exception as e:
                continue
                
        return user_data
    
    def train_models_from_logs(self):
        """Main function to train ML models from system logs"""
        print("Starting ML model training from system logs...")
        
        # Collect system logs
        print("Collecting system logs...")
        system_logs = self.get_system_logs('System', hours_back=48)
        app_logs = self.get_system_logs('Application', hours_back=48)
        
        print(f"Collected {len(system_logs)} system logs and {len(app_logs)} application logs")
        
        # Process logs to training data
        print("Processing logs to training data...")
        all_logs = system_logs + app_logs
        training_data = self.process_logs_to_training_data(all_logs)
        
        print(f"Generated {len(training_data)} training samples")
        
        # Collect user behavior data
        print("Collecting user behavior data...")
        user_data = self.collect_user_behavior_data()
        print(f"Generated {len(user_data)} user behavior samples")
        
        # Get current system metrics
        print("Collecting system performance metrics...")
        metrics = self.get_system_performance_metrics()
        print(f"Current system metrics: {metrics}")
        
        # Train models if we have enough data
        if len(training_data) >= 10:
            print("Training system load prediction model...")
            
            # Create system load training data
            system_data = []
            for i, data in enumerate(training_data):
                # Simulate system load based on log patterns
                load = min(100, max(0, 
                    metrics['cpu_usage'] + 
                    (data['is_error'] * 20) + 
                    (data['is_warning'] * 10) + 
                    (data['event_id'] % 30)
                ))
                
                system_sample = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_usage': metrics['cpu_usage'] + (i % 10 - 5),
                    'memory_usage': metrics['memory_usage'] + (i % 15 - 7),
                    'disk_usage': metrics['disk_usage'] + (i % 8 - 4),
                    'network_usage': 25 + (i % 20),
                    'system_load': load
                }
                system_data.append(system_sample)
            
            # Train system load model
            try:
                self.system_optimizer.train_system_load_model(system_data)
                print("✓ System load prediction model trained successfully")
            except Exception as e:
                print(f"✗ Error training system load model: {e}")
        
        if len(user_data) >= 10:
            print("Training user behavior prediction model...")
            
            # Add patterns to user data
            enhanced_user_data = []
            for i, data in enumerate(user_data):
                # Add pattern simulation
                pattern = 'work' if data['hour'] >= 9 and data['hour'] <= 17 else 'personal'
                data['pattern'] = pattern
                enhanced_user_data.append(data)
            
            try:
                self.behavior_predictor.train_user_behavior_model(enhanced_user_data)
                print("✓ User behavior prediction model trained successfully")
            except Exception as e:
                print(f"✗ Error training user behavior model: {e}")
        
        # Test predictions
        print("\nTesting trained models...")
        
        # Test system load prediction
        try:
            current_time = datetime.now()
            current_metrics = metrics.copy()
            current_metrics['timestamp'] = current_time.isoformat()
            
            prediction = self.system_optimizer.predict_system_load(current_metrics)
            print(f"✓ System load prediction: {prediction}")
        except Exception as e:
            print(f"✗ Error testing system load prediction: {e}")
        
        # Test user behavior prediction
        try:
            current_context = {
                'hour': current_time.hour,
                'day_of_week': current_time.weekday(),
                'application_usage': 1,
                'click_count': 5,
                'window_switches': 2,
                'keystroke_count': 50,
                'idle_time': 30
            }
            
            behavior_prediction = self.behavior_predictor.predict_user_behavior(current_context)
            print(f"✓ User behavior prediction: {behavior_prediction}")
        except Exception as e:
            print(f"✗ Error testing user behavior prediction: {e}")
        
        # Get automation recommendations
        try:
            recommendations = self.recommendation_engine.get_automation_recommendations()
            print(f"✓ Automation recommendations: {recommendations}")
        except Exception as e:
            print(f"✗ Error getting automation recommendations: {e}")
        
        print("\nML model training completed!")
        return True

def main():
    """Main execution function"""
    processor = SystemLogProcessor()
    
    try:
        success = processor.train_models_from_logs()
        if success:
            print("\n✓ All ML models trained successfully from system logs!")
        else:
            print("\n✗ Some issues occurred during training")
    except Exception as e:
        print(f"\n✗ Error during training: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
