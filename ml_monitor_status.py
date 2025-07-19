#!/usr/bin/env python3
"""
ML Monitor Status Tool
Comprehensive monitoring dashboard for ML system status, data collection progress, and training readiness.
"""

import json
import sqlite3
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
from typing import Dict, List, Any, Optional

class MLMonitorStatus:
    def __init__(self, base_dir: str = None):
        """Initialize ML Monitor Status with base directory."""
        if base_dir is None:
            base_dir = Path(__file__).parent
        self.base_dir = Path(base_dir)
        
        # File paths
        self.ml_data_file = self.base_dir / "ml_data.json"
        self.user_activity_db = self.base_dir / "user_activity.db"
        self.bridge_log = self.base_dir / "bridge_activity.log"
        
        # ML training thresholds
        self.min_samples_behavior = 100
        self.min_samples_system = 100
        self.min_samples_adaptive = 50
        
    def load_ml_data(self) -> Dict[str, Any]:
        """Load ML data from JSON file."""
        try:
            if self.ml_data_file.exists():
                with open(self.ml_data_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading ML data: {e}")
            return {}
    
    def get_sqlite_stats(self) -> Dict[str, Any]:
        """Get statistics from SQLite user activity database."""
        stats = {
            "total_records": 0,
            "recent_24h": 0,
            "recent_1h": 0,
            "activity_types": {},
            "latest_timestamp": None,
            "oldest_timestamp": None
        }
        
        try:
            if not self.user_activity_db.exists():
                return stats
                
            conn = sqlite3.connect(str(self.user_activity_db))
            cursor = conn.cursor()
            
            # Total records
            cursor.execute("SELECT COUNT(*) FROM user_activity")
            stats["total_records"] = cursor.fetchone()[0]
            
            # Recent activity (24h and 1h)
            now = datetime.now()
            day_ago = now - timedelta(hours=24)
            hour_ago = now - timedelta(hours=1)
            
            cursor.execute("""
                SELECT COUNT(*) FROM user_activity 
                WHERE timestamp > ?
            """, (day_ago.isoformat(),))
            stats["recent_24h"] = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM user_activity 
                WHERE timestamp > ?
            """, (hour_ago.isoformat(),))
            stats["recent_1h"] = cursor.fetchone()[0]
            
            # Activity types distribution
            cursor.execute("""
                SELECT activity_type, COUNT(*) 
                FROM user_activity 
                GROUP BY activity_type
            """)
            for activity_type, count in cursor.fetchall():
                stats["activity_types"][activity_type] = count
            
            # Timestamp range
            cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM user_activity")
            min_ts, max_ts = cursor.fetchone()
            stats["oldest_timestamp"] = min_ts
            stats["latest_timestamp"] = max_ts
            
            conn.close()
            
        except Exception as e:
            print(f"Error querying SQLite database: {e}")
            
        return stats
    
    def check_process_status(self) -> Dict[str, bool]:
        """Check if monitoring processes are running."""
        status = {
            "unified_server": False,
            "integrated_monitoring": False,
            "ml_engine": False
        }
        
        try:
            # Check for Python processes related to monitoring
            result = subprocess.run([
                "powershell", "-Command",
                "Get-Process python* | Where-Object {$_.CommandLine -like '*monitor*' -or $_.CommandLine -like '*ml*' -or $_.CommandLine -like '*unified*'} | Select-Object ProcessName, CommandLine"
            ], capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                output = result.stdout.lower()
                if "unified" in output or "server" in output:
                    status["unified_server"] = True
                if "monitor" in output or "bridge" in output:
                    status["integrated_monitoring"] = True
                if "ml" in output:
                    status["ml_engine"] = True
                    
        except Exception as e:
            print(f"Error checking process status: {e}")
            
        return status
    
    def get_bridge_activity(self) -> Dict[str, Any]:
        """Get information about bridge activity from logs."""
        bridge_info = {
            "log_exists": False,
            "recent_entries": 0,
            "last_activity": None,
            "total_size_kb": 0
        }
        
        try:
            if self.bridge_log.exists():
                bridge_info["log_exists"] = True
                stat = self.bridge_log.stat()
                bridge_info["total_size_kb"] = stat.st_size / 1024
                
                # Read recent log entries (last 100 lines)
                with open(self.bridge_log, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        bridge_info["recent_entries"] = len(lines)
                        # Try to parse last timestamp
                        last_line = lines[-1].strip()
                        if last_line:
                            bridge_info["last_activity"] = last_line[:20]  # Approximate timestamp
                            
        except Exception as e:
            print(f"Error reading bridge log: {e}")
            
        return bridge_info
    
    def calculate_training_readiness(self, ml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate training readiness for each ML model."""
        readiness = {
            "behavior_prediction": {
                "current_samples": len(ml_data.get("user_actions", [])),
                "required_samples": self.min_samples_behavior,
                "ready": False,
                "progress_percent": 0
            },
            "system_optimization": {
                "current_samples": len(ml_data.get("system_metrics", [])),
                "required_samples": self.min_samples_system,
                "ready": False,
                "progress_percent": 0
            },
            "adaptive_learning": {
                "current_samples": len(ml_data.get("user_feedback", [])),
                "required_samples": self.min_samples_adaptive,
                "ready": False,
                "progress_percent": 0
            }
        }
        
        for model_type, info in readiness.items():
            current = info["current_samples"]
            required = info["required_samples"]
            info["progress_percent"] = min(100, (current / required) * 100)
            info["ready"] = current >= required
            
        return readiness
    
    def get_data_quality_metrics(self, ml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data quality metrics."""
        quality = {
            "data_freshness": "Unknown",
            "data_diversity": 0,
            "collection_rate": "Unknown",
            "consistency_score": 0
        }
        
        try:
            # Check data freshness (most recent entry)
            user_actions = ml_data.get("user_actions", [])
            if user_actions:
                latest_action = max(user_actions, key=lambda x: x.get("timestamp", ""))
                latest_time = datetime.fromisoformat(latest_action.get("timestamp", ""))
                time_diff = datetime.now() - latest_time
                if time_diff.total_seconds() < 3600:  # Less than 1 hour
                    quality["data_freshness"] = "Fresh"
                elif time_diff.total_seconds() < 24*3600:  # Less than 24 hours
                    quality["data_freshness"] = "Recent"
                else:
                    quality["data_freshness"] = "Stale"
            
            # Data diversity (unique activity types)
            activity_types = set()
            for action in user_actions:
                activity_types.add(action.get("type", "unknown"))
            quality["data_diversity"] = len(activity_types)
            
            # Collection rate estimate (actions per hour in last 24h)
            recent_actions = []
            cutoff_time = datetime.now() - timedelta(hours=24)
            for action in user_actions:
                action_time = datetime.fromisoformat(action.get("timestamp", ""))
                if action_time > cutoff_time:
                    recent_actions.append(action)
            
            if recent_actions:
                quality["collection_rate"] = f"{len(recent_actions)/24:.1f} actions/hour"
            
        except Exception as e:
            print(f"Error calculating data quality: {e}")
            
        return quality
    
    def print_status_report(self):
        """Print comprehensive status report."""
        print("=" * 80)
        print("🤖 ML MONITOR STATUS DASHBOARD")
        print("=" * 80)
        print(f"⏰ Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Load data
        ml_data = self.load_ml_data()
        sqlite_stats = self.get_sqlite_stats()
        process_status = self.check_process_status()
        bridge_info = self.get_bridge_activity()
        training_readiness = self.calculate_training_readiness(ml_data)
        data_quality = self.get_data_quality_metrics(ml_data)
        
        # System Status
        print("📊 SYSTEM STATUS")
        print("-" * 40)
        status_indicators = {
            "unified_server": "🟢" if process_status["unified_server"] else "🔴",
            "integrated_monitoring": "🟢" if process_status["integrated_monitoring"] else "🔴",
            "ml_engine": "🟢" if process_status["ml_engine"] else "🔴"
        }
        
        print(f"  Unified Server:        {status_indicators['unified_server']} {'Running' if process_status['unified_server'] else 'Stopped'}")
        print(f"  Integrated Monitoring: {status_indicators['integrated_monitoring']} {'Active' if process_status['integrated_monitoring'] else 'Inactive'}")
        print(f"  ML Engine:            {status_indicators['ml_engine']} {'Running' if process_status['ml_engine'] else 'Stopped'}")
        print()
        
        # Data Collection Summary
        print("📈 DATA COLLECTION SUMMARY")
        print("-" * 40)
        print(f"  ML JSON Data:")
        print(f"    User Actions:     {len(ml_data.get('user_actions', []))} samples")
        print(f"    System Metrics:   {len(ml_data.get('system_metrics', []))} samples")
        print(f"    User Feedback:    {len(ml_data.get('user_feedback', []))} samples")
        print()
        print(f"  SQLite Activity DB:")
        print(f"    Total Records:    {sqlite_stats['total_records']} entries")
        print(f"    Recent (24h):     {sqlite_stats['recent_24h']} entries")
        print(f"    Recent (1h):      {sqlite_stats['recent_1h']} entries")
        print()
        
        # Activity Types Breakdown
        if sqlite_stats["activity_types"]:
            print("  Activity Types:")
            for activity_type, count in sorted(sqlite_stats["activity_types"].items()):
                print(f"    {activity_type:<15}: {count} entries")
            print()
        
        # Training Readiness
        print("🎯 TRAINING READINESS")
        print("-" * 40)
        for model_name, info in training_readiness.items():
            ready_indicator = "✅" if info["ready"] else "⏳"
            progress_bar = "█" * int(info["progress_percent"] / 10) + "░" * (10 - int(info["progress_percent"] / 10))
            print(f"  {model_name.replace('_', ' ').title()}:")
            print(f"    {ready_indicator} {info['current_samples']}/{info['required_samples']} samples ({info['progress_percent']:.1f}%)")
            print(f"    [{progress_bar}]")
            print()
        
        # Data Quality
        print("✨ DATA QUALITY METRICS")
        print("-" * 40)
        freshness_indicator = {"Fresh": "🟢", "Recent": "🟡", "Stale": "🔴", "Unknown": "⚪"}.get(data_quality["data_freshness"], "⚪")
        print(f"  Data Freshness:    {freshness_indicator} {data_quality['data_freshness']}")
        print(f"  Activity Diversity: {data_quality['data_diversity']} unique types")
        print(f"  Collection Rate:    {data_quality['collection_rate']}")
        print()
        
        # Bridge Integration Status
        print("🌉 INTEGRATION BRIDGE STATUS")
        print("-" * 40)
        bridge_indicator = "🟢" if bridge_info["log_exists"] else "🔴"
        print(f"  Bridge Log:        {bridge_indicator} {'Active' if bridge_info['log_exists'] else 'Not Found'}")
        if bridge_info["log_exists"]:
            print(f"  Log Size:          {bridge_info['total_size_kb']:.1f} KB")
            print(f"  Recent Entries:    {bridge_info['recent_entries']} lines")
            if bridge_info["last_activity"]:
                print(f"  Last Activity:     {bridge_info['last_activity']}")
        print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS")
        print("-" * 40)
        recommendations = []
        
        # Check if any processes are down
        if not any(process_status.values()):
            recommendations.append("🔴 No monitoring processes detected - start unified server")
        
        # Check data collection progress
        total_samples = len(ml_data.get('user_actions', [])) + len(ml_data.get('system_metrics', []))
        if total_samples < 50:
            recommendations.append("📊 Low data collection - continue normal activity to accumulate samples")
        elif total_samples < 150:
            recommendations.append("⏳ Moderate data collection - approaching training threshold")
        else:
            recommendations.append("✅ Sufficient data collected - ready for ML model training")
        
        # Check data freshness
        if data_quality["data_freshness"] == "Stale":
            recommendations.append("⚠️  Data appears stale - verify monitoring is active")
        
        # Check bridge status
        if not bridge_info["log_exists"]:
            recommendations.append("🌉 Bridge integration log not found - verify integrated monitoring")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  ✅ All systems operational - continue monitoring")
        
        print()
        print("=" * 80)
    
    def export_status_json(self, output_file: str = None):
        """Export status data as JSON for programmatic access."""
        if output_file is None:
            output_file = self.base_dir / "ml_status_report.json"
        
        ml_data = self.load_ml_data()
        sqlite_stats = self.get_sqlite_stats()
        process_status = self.check_process_status()
        bridge_info = self.get_bridge_activity()
        training_readiness = self.calculate_training_readiness(ml_data)
        data_quality = self.get_data_quality_metrics(ml_data)
        
        status_report = {
            "timestamp": datetime.now().isoformat(),
            "system_status": process_status,
            "data_collection": {
                "ml_json": {
                    "user_actions": len(ml_data.get('user_actions', [])),
                    "system_metrics": len(ml_data.get('system_metrics', [])),
                    "user_feedback": len(ml_data.get('user_feedback', []))
                },
                "sqlite_activity": sqlite_stats
            },
            "training_readiness": training_readiness,
            "data_quality": data_quality,
            "bridge_status": bridge_info
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(status_report, f, indent=2)
            print(f"📄 Status report exported to: {output_file}")
        except Exception as e:
            print(f"Error exporting status report: {e}")

def main():
    """Main entry point for ML Monitor Status tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ML Monitor Status Tool")
    parser.add_argument("--json", "-j", help="Export status as JSON file")
    parser.add_argument("--watch", "-w", action="store_true", help="Watch mode - refresh every 30 seconds")
    parser.add_argument("--dir", "-d", help="Base directory for ML monitoring files")
    
    args = parser.parse_args()
    
    monitor = MLMonitorStatus(args.dir)
    
    if args.watch:
        print("👀 Watch mode enabled - Press Ctrl+C to exit")
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
                monitor.print_status_report()
                print("🔄 Refreshing in 30 seconds... (Ctrl+C to exit)")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 Exiting watch mode")
    else:
        monitor.print_status_report()
    
    if args.json:
        monitor.export_status_json(args.json)

if __name__ == "__main__":
    main()
