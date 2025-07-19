#!/usr/bin/env python3
"""
Quick data collection script to rapidly build ML training dataset
"""

import sys
import time
import threading
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ml_predictive_engine import get_ml_engine

def collect_data_rapidly(count=50, interval=2):
    """Collect system data rapidly"""
    print(f"🚀 Starting rapid data collection: {count} samples every {interval} seconds")
    
    try:
        # Get ML engine
        ml_engine = get_ml_engine()
        data_collector = ml_engine['data_collector']
        
        print(f"📊 Starting metrics: {len(data_collector.metrics)} recorded")
        
        for i in range(count):
            try:
                # Record system metrics
                data_collector.record_system_metrics()
                
                # Log some sample user actions
                if i % 10 == 0:  # Every 10th iteration
                    data_collector.record_action("system_monitoring", "ml_engine", 1.0, True)
                
                print(f"✅ Collected sample {i+1}/{count} - Total: {len(data_collector.metrics)} metrics, {len(data_collector.actions)} actions")
                
                if i < count - 1:  # Don't sleep after last iteration
                    time.sleep(interval)
                    
            except KeyboardInterrupt:
                print(f"\n⏹️ Collection stopped by user at sample {i+1}")
                break
            except Exception as e:
                print(f"❌ Error at sample {i+1}: {e}")
                continue
        
        print(f"\n🎉 Data collection complete!")
        print(f"📈 Final totals: {len(data_collector.metrics)} metrics, {len(data_collector.actions)} actions")
        
        # Try training if we have enough data
        if len(data_collector.metrics) >= 100:
            print(f"\n🤖 Attempting to train system optimizer...")
            try:
                result = ml_engine['system_optimizer'].train_model()
                if 'error' in result:
                    print(f"Training failed: {result['error']}")
                else:
                    print(f"✅ System optimizer trained successfully!")
                    print(f"Train MSE: {result['train_mse']:.4f}")
                    print(f"Test MSE: {result['test_mse']:.4f}")
                    print(f"Samples used: {result['samples_used']}")
            except Exception as e:
                print(f"❌ Training error: {e}")
        else:
            print(f"📊 Need {100 - len(data_collector.metrics)} more metrics for system optimizer training")
        
        return len(data_collector.metrics), len(data_collector.actions)
        
    except Exception as e:
        print(f"❌ Collection failed: {e}")
        return 0, 0

if __name__ == "__main__":
    print("=== Quick ML Data Collection ===")
    
    # Collect data rapidly
    metrics_count, actions_count = collect_data_rapidly(50, 2)
    
    print(f"\n✅ Collection session complete: {metrics_count} metrics, {actions_count} actions")
