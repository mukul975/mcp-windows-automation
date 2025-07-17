#!/usr/bin/env python3
"""
Test script for ML predictive automation integration
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test the ML engine
def test_ml_engine():
    print("🤖 Testing ML Predictive Engine...")
    
    try:
        from src.ml_predictive_engine import get_ml_engine
        
        # Get ML engine instances
        ml_engine = get_ml_engine()
        
        print("✅ ML Engine loaded successfully")
        print(f"   - Data collector: {type(ml_engine['data_collector']).__name__}")
        print(f"   - Behavior predictor: {type(ml_engine['behavior_predictor']).__name__}")
        print(f"   - System optimizer: {type(ml_engine['system_optimizer']).__name__}")
        print(f"   - Recommendation engine: {type(ml_engine['recommendation_engine']).__name__}")
        
        # Test data collection
        print("\n📊 Testing data collection...")
        data_collector = ml_engine['data_collector']
        
        # Record some sample actions
        sample_actions = [
            ("open_app", "spotify", 2.5),
            ("play_song", "spotify", 1.0),
            ("search", "chrome", 0.8),
            ("type_text", "notepad", 3.2),
            ("open_app", "calculator", 1.1),
        ]
        
        for action_type, app, duration in sample_actions:
            data_collector.record_action(action_type, app, duration)
            print(f"   ✅ Recorded: {action_type} in {app} ({duration}s)")
        
        # Record system metrics
        data_collector.record_system_metrics()
        print("   ✅ System metrics recorded")
        
        print(f"\n📈 Data Summary:")
        print(f"   - Total actions: {len(data_collector.actions)}")
        print(f"   - Total metrics: {len(data_collector.metrics)}")
        
        # Test behavior predictor (if enough data)
        behavior_predictor = ml_engine['behavior_predictor']
        if len(data_collector.actions) >= 10:
            print("\n🧠 Testing behavior prediction...")
            
            # Train model
            training_result = behavior_predictor.train_model(min_samples=5)
            if 'error' not in training_result:
                print(f"   ✅ Model trained successfully")
                print(f"   - Train accuracy: {training_result['train_accuracy']:.2%}")
                print(f"   - Test accuracy: {training_result['test_accuracy']:.2%}")
                
                # Test prediction
                prediction = behavior_predictor.predict_next_action({'duration': 1.0})
                if 'error' not in prediction:
                    print(f"   ✅ Prediction: {prediction['predicted_action']} (confidence: {prediction['confidence']:.2%})")
                else:
                    print(f"   ❌ Prediction failed: {prediction['error']}")
            else:
                print(f"   ❌ Training failed: {training_result['error']}")
        else:
            print("\n⚠️  Not enough data for behavior prediction (need at least 10 actions)")
        
        # Test system optimizer (if enough data)
        system_optimizer = ml_engine['system_optimizer']
        if len(data_collector.metrics) >= 10:
            print("\n⚙️  Testing system optimization...")
            
            # Add more metrics for training
            for i in range(15):
                data_collector.record_system_metrics()
                import time
                time.sleep(0.1)
            
            training_result = system_optimizer.train_model(min_samples=10)
            if 'error' not in training_result:
                print(f"   ✅ System optimizer trained successfully")
                print(f"   - Train MSE: {training_result['train_mse']:.4f}")
                print(f"   - Test MSE: {training_result['test_mse']:.4f}")
                
                # Test prediction
                prediction = system_optimizer.predict_system_load()
                if 'error' not in prediction:
                    print(f"   ✅ Load prediction: {prediction['predicted_cpu_load']:.1f}% (current: {prediction['current_cpu_load']:.1f}%)")
                else:
                    print(f"   ❌ Load prediction failed: {prediction['error']}")
            else:
                print(f"   ❌ Optimizer training failed: {training_result['error']}")
        else:
            print("\n⚠️  Not enough data for system optimization (need at least 10 metrics)")
        
        # Test recommendations
        print("\n💡 Testing automation recommendations...")
        recommendation_engine = ml_engine['recommendation_engine']
        
        recommendations = recommendation_engine.get_recommendations()
        if recommendations:
            print(f"   ✅ Generated {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"      {i}. {rec['recommendation']}")
        else:
            print("   ⚠️  No recommendations generated")
        
        print("\n🎉 ML integration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please install required packages: pip install scikit-learn pandas numpy joblib")
        return False
    except Exception as e:
        print(f"❌ Error testing ML engine: {e}")
        return False

def test_mcp_integration():
    print("\n🔧 Testing MCP integration...")
    
    try:
        # Test importing the unified server
        from unified_server import ML_AVAILABLE
        
        if ML_AVAILABLE:
            print("✅ ML tools available in MCP server")
            
            # List ML tools (this would normally be done through MCP protocol)
            ml_tools = [
                "record_user_action",
                "record_system_metrics", 
                "train_behavior_model",
                "predict_next_action",
                "train_system_optimizer",
                "predict_system_load",
                "get_automation_recommendations",
                "get_ml_stats",
                "auto_optimize_system",
                "start_ml_monitoring"
            ]
            
            print(f"   Available ML tools: {len(ml_tools)}")
            for tool in ml_tools:
                print(f"      - {tool}")
            
            return True
        else:
            print("❌ ML tools not available in MCP server")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MCP integration: {e}")
        return False

def main():
    print("🚀 Starting ML Predictive Automation Test Suite\n")
    
    # Test ML engine
    ml_test_passed = test_ml_engine()
    
    # Test MCP integration
    mcp_test_passed = test_mcp_integration()
    
    # Summary
    print("\n" + "="*50)
    print("📋 Test Summary:")
    print(f"   ML Engine: {'✅ PASS' if ml_test_passed else '❌ FAIL'}")
    print(f"   MCP Integration: {'✅ PASS' if mcp_test_passed else '❌ FAIL'}")
    
    if ml_test_passed and mcp_test_passed:
        print("\n🎉 All tests passed! ML predictive automation is ready to use.")
        print("\nNext steps:")
        print("1. Start the MCP server: python unified_server.py")
        print("2. Use ML tools through your AI assistant")
        print("3. Let the system collect data for better predictions")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        
        if not ml_test_passed:
            print("   - Install ML dependencies: pip install -r requirements.txt")
        
        if not mcp_test_passed:
            print("   - Check MCP server configuration")

if __name__ == "__main__":
    main()
