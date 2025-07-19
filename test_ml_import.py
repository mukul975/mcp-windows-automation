#!/usr/bin/env python3
"""
Test script to debug ML import issues
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("=== ML Import Debug Test ===")
print(f"Current directory: {current_dir}")
print(f"Python path: {sys.path[:3]}...")  # Show first 3 paths

# Test 1: Basic ML library imports
print("\n1. Testing ML library imports...")
try:
    import sklearn
    import pandas
    import numpy
    import joblib
    print("   ✅ All ML libraries available")
except ImportError as e:
    print(f"   ❌ ML library import failed: {e}")
    sys.exit(1)

# Test 2: Test src directory exists
print("\n2. Testing src directory...")
src_dir = current_dir / "src"
if src_dir.exists():
    print(f"   ✅ src directory exists: {src_dir}")
    
    ml_file = src_dir / "ml_predictive_engine.py"
    if ml_file.exists():
        print(f"   ✅ ml_predictive_engine.py exists: {ml_file}")
    else:
        print(f"   ❌ ml_predictive_engine.py NOT found")
        sys.exit(1)
else:
    print(f"   ❌ src directory NOT found: {src_dir}")
    sys.exit(1)

# Test 3: Try importing the ML engine
print("\n3. Testing ML engine import...")
try:
    from src.ml_predictive_engine import get_ml_engine
    print("   ✅ ML engine import successful")
    
    # Test 4: Try initializing the engine
    print("\n4. Testing ML engine initialization...")
    ml_engine = get_ml_engine()
    print(f"   ✅ ML engine initialized")
    print(f"   - Data collector: {type(ml_engine['data_collector']).__name__}")
    print(f"   - Behavior predictor: {type(ml_engine['behavior_predictor']).__name__}")
    print(f"   - System optimizer: {type(ml_engine['system_optimizer']).__name__}")
    print(f"   - Recommendation engine: {type(ml_engine['recommendation_engine']).__name__}")
    
    # Test 5: Try basic functionality
    print("\n5. Testing basic ML functionality...")
    data_collector = ml_engine['data_collector']
    
    # Record a test metric
    data_collector.record_system_metrics()
    print(f"   ✅ System metrics recorded. Total metrics: {len(data_collector.metrics)}")
    
    # Record a test action
    data_collector.record_action("test_action", "test_app", 1.0, True)
    print(f"   ✅ User action recorded. Total actions: {len(data_collector.actions)}")
    
    print("\n✅ ALL TESTS PASSED - ML engine is working correctly!")
    
except ImportError as e:
    print(f"   ❌ ML engine import failed: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"   ❌ ML engine error: {e}")
    import traceback
    traceback.print_exc()
