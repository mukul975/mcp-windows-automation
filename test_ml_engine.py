#!/usr/bin/env python3
"""
Test script for the ML predictive engine.
Collects system data, generates sample user actions, trains models, and tests predictions.
"""

import sys
import time
sys.path.append('.')
from ml_predictive_engine import PredictiveEngine

def main():
    # Initialize the ML engine
    engine = PredictiveEngine()
    
    # Collect some initial system data points
    print('Collecting initial system data...')
    for i in range(10):
        engine.collect_system_data()
        time.sleep(1)  # Wait 1 second between collections
        print(f'Data point {i+1}/10 collected')
    
    # Collect some mock user actions to have training data
    print('\nGenerating sample user actions...')
    sample_actions = [
        {'action': 'open_app', 'app': 'notepad', 'timestamp': time.time()},
        {'action': 'click', 'x': 100, 'y': 200, 'timestamp': time.time()},
        {'action': 'type', 'text': 'hello world', 'timestamp': time.time()},
        {'action': 'open_app', 'app': 'chrome', 'timestamp': time.time()},
        {'action': 'click', 'x': 300, 'y': 400, 'timestamp': time.time()},
    ]
    
    for action in sample_actions:
        engine.collect_user_action(action)
        print(f'Recorded action: {action["action"]}')
    
    # Train the models
    print('\nTraining ML models...')
    try:
        engine.train_models()
        print('Models trained successfully!')
    except Exception as e:
        print(f'Training error: {e}')
    
    # Test predictions
    print('\nTesting predictions...')
    try:
        load_pred = engine.predict_system_load()
        print(f'System load prediction: {load_pred}')
        
        behavior_pred = engine.predict_user_behavior()
        print(f'User behavior prediction: {behavior_pred}')
        
        recommendations = engine.get_optimization_recommendations()
        print(f'Optimization recommendations: {recommendations}')
    except Exception as e:
        print(f'Prediction error: {e}')

if __name__ == '__main__':
    main()
