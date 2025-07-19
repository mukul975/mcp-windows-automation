#!/usr/bin/env python3
"""
ML Stats Monitor - Displays ML engine statistics every 21 seconds
"""

import sys
import time
import os
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ml_stats():
    """Get ML engine statistics"""
    try:
        from src.ml_predictive_engine import get_ml_engine
        ML_ENGINE = get_ml_engine()
        
        data_collector = ML_ENGINE['data_collector']
        behavior_predictor = ML_ENGINE['behavior_predictor']
        system_optimizer = ML_ENGINE['system_optimizer']
        
        stats = f"📊 ML Engine Statistics:\n\n"
        stats += f"Data Collection:\n"
        stats += f"  - User actions recorded: {len(data_collector.actions)}\n"
        stats += f"  - System metrics recorded: {len(data_collector.metrics)}\n\n"
        
        stats += f"Model Status:\n"
        stats += f"  - Behavior predictor trained: {'✅' if behavior_predictor.is_trained else '❌'}\n"
        stats += f"  - System optimizer trained: {'✅' if system_optimizer.is_trained else '❌'}\n\n"
        
        # Progress toward training requirements
        stats += f"Training Progress:\n"
        stats += f"  - System Optimizer: {len(data_collector.metrics)}/100 metrics ({(len(data_collector.metrics)/100*100):.1f}%)\n"
        stats += f"  - Behavior Predictor: {len(data_collector.actions)}/50 actions ({(len(data_collector.actions)/50*100) if len(data_collector.actions) < 50 else 100:.1f}%)\n\n"
        
        # Recent activity
        if len(data_collector.metrics) > 0:
            last_metric = data_collector.metrics[-1]
            stats += f"Latest System Metrics:\n"
            stats += f"  - CPU Usage: {last_metric.cpu_usage:.1f}%\n"
            stats += f"  - Memory Usage: {last_metric.memory_usage:.1f}%\n"
            stats += f"  - Disk Usage: {last_metric.disk_usage:.1f}%\n"
            stats += f"  - Active Processes: {last_metric.active_processes}\n"
            stats += f"  - Last Updated: {last_metric.timestamp.strftime('%H:%M:%S')}\n\n"
        
        if len(data_collector.actions) > 0:
            recent_actions = data_collector.actions[-3:]
            stats += f"Recent Actions:\n"
            for action in recent_actions:
                stats += f"  - {action.action_type} in {action.application} at {action.timestamp.strftime('%H:%M:%S')}\n"
        
        return stats
        
    except ImportError:
        return "❌ ML engine not available - check dependencies"
    except Exception as e:
        return f"❌ Error getting ML stats: {str(e)}"

def main():
    """Main monitoring loop"""
    print("🔍 ML Stats Monitor Starting...")
    print("📊 Checking ML engine status every 21 seconds")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        iteration = 0
        while True:
            iteration += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Clear screen and show stats
            clear_screen()
            print(f"🔍 ML Stats Monitor (Update #{iteration})")
            print(f"🕐 Current Time: {current_time}")
            print(f"⏱️  Next Update: {21} seconds")
            print("=" * 60)
            print()
            
            # Get and display ML stats
            stats = get_ml_stats()
            print(stats)
            
            print("=" * 60)
            print("🛑 Press Ctrl+C to stop monitoring")
            
            # Wait 21 seconds
            time.sleep(21)
            
    except KeyboardInterrupt:
        print("\n\n🛑 ML Stats Monitor stopped by user")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Monitor error: {e}")

if __name__ == "__main__":
    main()
