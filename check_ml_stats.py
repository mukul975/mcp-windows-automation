#!/usr/bin/env python3

import os
import sys
import json

# Add the parent directory to sys.path to import the ml_engine module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    from ml_engine.adaptive_ml_engine import AdaptiveMLEngine
    
    # Initialize ML engine
    engine = AdaptiveMLEngine()
    
    # Get statistics
    stats = engine.get_statistics()
    
    print("ML Engine Statistics:")
    print("====================")
    print(f"User Actions: {stats['user_actions']}")
    print(f"System Metrics: {stats['system_metrics']}")
    print(f"Behavior Predictor Trained: {stats['behavior_predictor_trained']}")
    print(f"System Optimizer Trained: {stats['system_optimizer_trained']}")
    
    if stats['behavior_predictor_trained']:
        print(f"Behavior Predictor Accuracy: {stats['behavior_predictor_accuracy']:.4f}")
    
    if stats['system_optimizer_trained']:
        print(f"System Optimizer Score: {stats['system_optimizer_score']:.4f}")
    
    print(f"\nTraining Requirements:")
    print(f"User Actions needed for Behavior Predictor: {max(0, 50 - stats['user_actions'])}")
    print(f"System Metrics needed for System Optimizer: {max(0, 100 - stats['system_metrics'])}")

except Exception as e:
    print(f"Error checking ML statistics: {e}")
