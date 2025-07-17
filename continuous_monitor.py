#!/usr/bin/env python3
"""
Continuous Security Monitoring Script
Runs security checks every 30 minutes
"""

import time
import psutil
import subprocess
import logging
from datetime import datetime, timedelta
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_monitor.log'),
        logging.StreamHandler()
    ]
)

def check_security_issues():
    """Check for potential security issues"""
    detected_issues = []
    
    # 1. Check for suspicious processes
    suspicious_processes = [
        'malware.exe', 'ransomware.exe', 'cryptolocker.exe', 'trojan.exe',
        'keylogger.exe', 'backdoor.exe', 'rootkit.exe', 'virus.exe',
        'spyware.exe', 'adware.exe', 'hijacker.exe', 'worm.exe'
    ]
    
    current_processes = []
    for proc in psutil.process_iter(['name', 'pid', 'cpu_percent', 'memory_percent']):
        try:
            current_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    for process in current_processes:
        if process['name'].lower() in [sp.lower() for sp in suspicious_processes]:
            detected_issues.append(f"🚨 SUSPICIOUS PROCESS: {process['name']} (PID: {process['pid']})")
    
    # 2. Check for high CPU/Memory usage processes
    high_cpu_processes = [p for p in current_processes if p['cpu_percent'] and p['cpu_percent'] > 90]
    high_memory_processes = [p for p in current_processes if p['memory_percent'] and p['memory_percent'] > 90]
    
    if high_cpu_processes:
        for proc in high_cpu_processes[:2]:  # Top 2
            detected_issues.append(f"⚠️ HIGH CPU: {proc['name']} ({proc['cpu_percent']:.1f}%)")
    
    if high_memory_processes:
        for proc in high_memory_processes[:2]:  # Top 2
            detected_issues.append(f"⚠️ HIGH MEMORY: {proc['name']} ({proc['memory_percent']:.1f}%)")
    
    # 3. Check disk space
    try:
        disk_usage = psutil.disk_usage('C:')
        free_percent = (disk_usage.free / disk_usage.total) * 100
        if free_percent < 5:
            detected_issues.append(f"💾 CRITICAL DISK SPACE: C: drive has only {free_percent:.1f}% free space")
        elif free_percent < 10:
            detected_issues.append(f"💾 LOW DISK SPACE: C: drive has only {free_percent:.1f}% free space")
    except Exception as e:
        detected_issues.append(f"⚠️ Could not check disk space: {str(e)}")
    
    # 4. Check Windows Defender status (simplified)
    try:
        defender_cmd = 'Get-MpComputerStatus | Select-Object AntivirusEnabled'
        result = subprocess.run(
            ["powershell", "-Command", defender_cmd],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout.strip():
            if "False" in result.stdout:
                detected_issues.append("🛡️ DEFENDER: Windows Defender may be disabled")
                
    except Exception as e:
        pass  # Skip if can't check
    
    # 5. Check for unusual network activity
    try:
        connections = psutil.net_connections(kind='inet')
        external_connections = [c for c in connections if c.status == 'ESTABLISHED' and c.raddr and not c.raddr.ip.startswith('127.')]
        
        if len(external_connections) > 50:
            detected_issues.append(f"🌐 NETWORK: {len(external_connections)} active external connections")
    except Exception as e:
        pass  # Skip if can't check
    
    return detected_issues, len(current_processes)

def monitor_continuously():
    """Monitor system continuously"""
    logging.info("🔒 Starting continuous security monitoring...")
    logging.info("📊 Monitoring interval: 30 minutes")
    logging.info("📁 Log file: security_monitor.log")
    
    while True:
        try:
            issues, process_count = check_security_issues()
            
            # Get system stats
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            if issues:
                logging.warning(f"🚨 SECURITY ISSUES DETECTED:")
                for issue in issues:
                    logging.warning(f"  {issue}")
            else:
                logging.info("✅ No security issues detected")
            
            # Log system status
            logging.info(f"📊 System Status: Processes={process_count}, CPU={cpu_percent}%, Memory={memory_percent}%")
            
            # Wait for 30 minutes (1800 seconds)
            time.sleep(1800)
            
        except KeyboardInterrupt:
            logging.info("🛑 Monitoring stopped by user")
            break
        except Exception as e:
            logging.error(f"❌ Error in monitoring: {str(e)}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    monitor_continuously()
