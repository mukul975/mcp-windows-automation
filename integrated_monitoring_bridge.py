#!/usr/bin/env python3
"""
Integrated Monitoring Bridge
Connects comprehensive user monitoring with ML engine data collection
to solve the dual-storage system issue.
"""

import os
import sys
import time
import threading
from datetime import datetime
from typing import Dict, Optional

# Add src directory to path for ML engine imports
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from ml_predictive_engine import get_ml_engine
    ML_ENGINE_AVAILABLE = True
    print("ML Engine successfully imported")
except ImportError as e:
    ML_ENGINE_AVAILABLE = False
    print(f"Warning: ML engine not available: {e}")

try:
    from comprehensive_user_monitor import ComprehensiveUserMonitor, UserActivity
    COMPREHENSIVE_MONITOR_AVAILABLE = True
    print("Comprehensive Monitor successfully imported")
except ImportError as e:
    COMPREHENSIVE_MONITOR_AVAILABLE = False
    print(f"Warning: Comprehensive monitor not available: {e}")

class IntegratedMonitoringBridge:
    """Bridge between comprehensive monitoring and ML engine"""
    
    def __init__(self):
        self.ml_engine = None
        self.comprehensive_monitor = None
        self.is_bridging = False
        self.bridge_thread = None
        
        # Initialize ML engine
        if ML_ENGINE_AVAILABLE:
            try:
                self.ml_engine = get_ml_engine()
                print("ML Engine initialized in bridge")
            except Exception as e:
                print(f"Error initializing ML engine: {e}")
                self.ml_engine = None
        
        # Initialize comprehensive monitor with custom record function
        if COMPREHENSIVE_MONITOR_AVAILABLE:
            try:
                self.comprehensive_monitor = ComprehensiveUserMonitor()
                # Override the record function to also feed ML engine
                self.comprehensive_monitor._original_record_activity = self.comprehensive_monitor._record_activity
                self.comprehensive_monitor._record_activity = self._bridge_record_activity
                print("Comprehensive monitor initialized with ML bridge")
            except Exception as e:
                print(f"Error initializing comprehensive monitor: {e}")
                self.comprehensive_monitor = None
    
    def _bridge_record_activity(self, activity: 'UserActivity'):
        """Enhanced record function that feeds both SQLite and ML engine"""
        try:
            # First, use the original recording function for SQLite storage
            if hasattr(self.comprehensive_monitor, '_original_record_activity'):
                self.comprehensive_monitor._original_record_activity(activity)
            
            # Then, also feed the ML engine if available
            if self.ml_engine and self.ml_engine['data_collector']:
                self._feed_ml_engine(activity)
                
        except Exception as e:
            print(f"Error in bridge record activity: {e}")
    
    def _feed_ml_engine(self, activity: 'UserActivity'):
        """Convert comprehensive monitor activity to ML engine format"""
        try:
            data_collector = self.ml_engine['data_collector']
            
            # Map comprehensive monitor activity types to ML engine format
            ml_action_type = self._map_activity_type(activity.activity_type)
            ml_application = self._clean_application_name(activity.application)
            ml_duration = getattr(activity, 'duration', 0.0) or 0.0
            
            # Record the action in ML engine
            data_collector.record_action(
                action_type=ml_action_type,
                application=ml_application,
                duration=ml_duration,
                success=True
            )
            
        except Exception as e:
            print(f"Error feeding ML engine: {e}")
    
    def _map_activity_type(self, activity_type: str) -> str:
        """Map comprehensive monitor activity types to ML engine types"""
        mapping = {
            'window_focus': 'window_focus',
            'mouse_click': 'mouse_click', 
            'key_press': 'keyboard_input',
            'app_launch': 'app_launch',
            'app_close': 'app_close',
            'url_visit': 'web_browse',
            'chrome_tab_open': 'web_browse',
            'file_access': 'file_operation'
        }
        return mapping.get(activity_type, activity_type)
    
    def _clean_application_name(self, app_name: str) -> str:
        """Clean and normalize application names"""
        if not app_name or app_name == 'Unknown':
            return 'system'
        
        # Remove .exe extension and clean up
        clean_name = app_name.lower().replace('.exe', '').strip()
        
        # Handle special cases
        if 'chrome' in clean_name:
            return 'chrome'
        elif 'firefox' in clean_name:
            return 'firefox'
        elif 'notepad' in clean_name:
            return 'notepad'
        elif 'explorer' in clean_name:
            return 'explorer'
        
        return clean_name[:50]  # Limit length
    
    def start_integrated_monitoring(self) -> bool:
        """Start integrated monitoring system"""
        if not COMPREHENSIVE_MONITOR_AVAILABLE:
            print("Error: Comprehensive monitor not available")
            return False
        
        if not ML_ENGINE_AVAILABLE or not self.ml_engine:
            print("Warning: ML engine not available - running monitoring only")
        
        try:
            # Start comprehensive monitoring
            success = self.comprehensive_monitor.start_monitoring()
            if success:
                print("Integrated monitoring started successfully")
                print("Data will be stored in both SQLite (comprehensive) and JSON (ML engine)")
                return True
            else:
                print("Error: Failed to start comprehensive monitoring")
                return False
                
        except Exception as e:
            print(f"Error starting integrated monitoring: {e}")
            return False
    
    def stop_integrated_monitoring(self) -> bool:
        """Stop integrated monitoring system"""
        try:
            if self.comprehensive_monitor and self.comprehensive_monitor.is_monitoring:
                self.comprehensive_monitor.stop_monitoring()
                print("Integrated monitoring stopped")
                return True
            else:
                print("Monitoring was not running")
                return False
                
        except Exception as e:
            print(f"Error stopping integrated monitoring: {e}")
            return False
    
    def get_monitoring_stats(self) -> Dict:
        """Get statistics from both monitoring systems"""
        stats = {
            'comprehensive_monitor': {},
            'ml_engine': {},
            'bridge_status': 'active' if self.is_bridging else 'inactive'
        }
        
        try:
            # Get comprehensive monitor stats
            if self.comprehensive_monitor:
                stats['comprehensive_monitor'] = {
                    'is_monitoring': self.comprehensive_monitor.is_monitoring,
                    'activities_count': len(self.comprehensive_monitor.activities),
                    'mouse_clicks': self.comprehensive_monitor.mouse_click_count,
                    'key_presses': self.comprehensive_monitor.key_press_count
                }
            
            # Get ML engine stats
            if self.ml_engine and self.ml_engine['data_collector']:
                data_collector = self.ml_engine['data_collector']
                stats['ml_engine'] = {
                    'actions_count': len(data_collector.actions),
                    'metrics_count': len(data_collector.metrics)
                }
                
        except Exception as e:
            stats['error'] = str(e)
        
        return stats

# Global instance
_integrated_bridge = None

def get_integrated_bridge():
    """Get or create the integrated monitoring bridge"""
    global _integrated_bridge
    if _integrated_bridge is None:
        _integrated_bridge = IntegratedMonitoringBridge()
    return _integrated_bridge

def start_integrated_monitoring():
    """Start integrated monitoring - convenience function"""
    bridge = get_integrated_bridge()
    return bridge.start_integrated_monitoring()

def stop_integrated_monitoring():
    """Stop integrated monitoring - convenience function"""
    bridge = get_integrated_bridge()
    return bridge.stop_integrated_monitoring()

def get_integrated_stats():
    """Get integrated monitoring stats - convenience function"""
    bridge = get_integrated_bridge()
    return bridge.get_monitoring_stats()

if __name__ == "__main__":
    print("Integrated Monitoring Bridge - Test Mode")
    
    bridge = get_integrated_bridge()
    
    print(f"ML Engine Available: {ML_ENGINE_AVAILABLE}")
    print(f"Comprehensive Monitor Available: {COMPREHENSIVE_MONITOR_AVAILABLE}")
    
    if bridge.start_integrated_monitoring():
        print("Monitoring started successfully!")
        
        try:
            # Run for 30 seconds as a test
            print("Running integrated monitoring for 30 seconds...")
            time.sleep(30)
            
            stats = bridge.get_monitoring_stats()
            print(f"Final stats: {stats}")
            
        except KeyboardInterrupt:
            print("\nStopping monitoring...")
        finally:
            bridge.stop_integrated_monitoring()
    else:
        print("Failed to start monitoring")
