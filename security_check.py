#!/usr/bin/env python3
"""
Standalone Security Monitoring Script
"""

import psutil
import subprocess
import time
from datetime import datetime

def check_security_issues():
    """Check for potential security issues"""
    print("🔒 SECURITY SCAN STARTING...")
    detected_issues = []
    
    # 1. Check for suspicious processes
    print("🔍 Checking for suspicious processes...")
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
    print("📊 Checking system resource usage...")
    high_cpu_processes = [p for p in current_processes if p['cpu_percent'] and p['cpu_percent'] > 80]
    high_memory_processes = [p for p in current_processes if p['memory_percent'] and p['memory_percent'] > 80]
    
    if high_cpu_processes:
        for proc in high_cpu_processes[:3]:  # Top 3
            detected_issues.append(f"⚠️ HIGH CPU: {proc['name']} ({proc['cpu_percent']:.1f}%)")
    
    if high_memory_processes:
        for proc in high_memory_processes[:3]:  # Top 3
            detected_issues.append(f"⚠️ HIGH MEMORY: {proc['name']} ({proc['memory_percent']:.1f}%)")
    
    # 3. Check Windows Security Event Log
    print("🔐 Checking Windows Security Event Log...")
    try:
        security_cmd = 'Get-WinEvent -FilterHashtable @{LogName="Security"; StartTime=(Get-Date).AddHours(-1)} -MaxEvents 10 | Where-Object {$_.LevelDisplayName -eq "Warning" -or $_.LevelDisplayName -eq "Error"}'
        result = subprocess.run(
            ["powershell", "-Command", security_cmd],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            security_events = result.stdout.strip().split('\n')
            event_count = len([line for line in security_events if line.strip()])
            if event_count > 0:
                detected_issues.append(f"🔐 SECURITY EVENTS: {event_count} warnings/errors in last hour")
                
    except Exception as e:
        detected_issues.append(f"⚠️ Could not check Security log: {str(e)}")
    
    # 4. Check System Event Log
    print("🖥️ Checking System Event Log...")
    try:
        system_cmd = 'Get-WinEvent -FilterHashtable @{LogName="System"; StartTime=(Get-Date).AddHours(-1)} -MaxEvents 10 | Where-Object {$_.LevelDisplayName -eq "Error"}'
        result = subprocess.run(
            ["powershell", "-Command", system_cmd],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            system_events = result.stdout.strip().split('\n')
            event_count = len([line for line in system_events if line.strip()])
            if event_count > 0:
                detected_issues.append(f"🖥️ SYSTEM ERRORS: {event_count} errors in last hour")
                
    except Exception as e:
        detected_issues.append(f"⚠️ Could not check System log: {str(e)}")
    
    # 5. Check for unusual network connections
    print("🌐 Checking network connections...")
    try:
        network_cmd = 'Get-NetTCPConnection | Where-Object {$_.State -eq "Established"} | Measure-Object'
        result = subprocess.run(
            ["powershell", "-Command", network_cmd],
            capture_output=True,
            text=True,
            timeout=20
        )
        
        if result.returncode == 0 and "Count" in result.stdout:
            # Extract connection count
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip().isdigit():
                    count = int(line.strip())
                    if count > 20:  # Many external connections
                        detected_issues.append(f"🌐 NETWORK: {count} active connections detected")
                    break
                    
    except Exception as e:
        detected_issues.append(f"⚠️ Could not check network connections: {str(e)}")
    
    # 6. Check Windows Defender status
    print("🛡️ Checking Windows Defender status...")
    try:
        defender_cmd = 'Get-MpComputerStatus'
        result = subprocess.run(
            ["powershell", "-Command", defender_cmd],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0 and result.stdout.strip():
            defender_output = result.stdout.strip()
            if "AntivirusEnabled" in defender_output and "False" in defender_output:
                detected_issues.append(f"🛡️ DEFENDER: Windows Defender may be disabled")
                
    except Exception as e:
        detected_issues.append(f"⚠️ Could not check Windows Defender: {str(e)}")
    
    # 7. Check disk space
    print("💾 Checking disk space...")
    try:
        disk_usage = psutil.disk_usage('C:')
        free_percent = (disk_usage.free / disk_usage.total) * 100
        if free_percent < 10:
            detected_issues.append(f"💾 LOW DISK SPACE: C: drive has only {free_percent:.1f}% free space")
    except Exception as e:
        detected_issues.append(f"⚠️ Could not check disk space: {str(e)}")
    
    # 8. Check for failed login attempts
    print("🔑 Checking for failed login attempts...")
    try:
        login_cmd = 'Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4625; StartTime=(Get-Date).AddHours(-1)} | Measure-Object'
        result = subprocess.run(
            ["powershell", "-Command", login_cmd],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0 and "Count" in result.stdout:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip().isdigit() and int(line.strip()) > 0:
                    detected_issues.append(f"🔑 LOGIN FAILURES: {line.strip()} failed login attempts in last hour")
                    break
                    
    except Exception as e:
        detected_issues.append(f"⚠️ Could not check login failures: {str(e)}")
    
    # Generate summary
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if detected_issues:
        print(f"\n🔒 SECURITY SCAN RESULTS ({timestamp})")
        print("=" * 50)
        for issue in detected_issues:
            print(issue)
    else:
        print(f"\n✅ NO SECURITY ISSUES DETECTED ({timestamp})")
    
    # System status
    print(f"\n📊 SYSTEM STATUS:")
    print(f"- Total Processes: {len(current_processes)}")
    print(f"- CPU Usage: {psutil.cpu_percent()}%")
    print(f"- Memory Usage: {psutil.virtual_memory().percent}%")
    print(f"- Disk Usage: {100 - (psutil.disk_usage('C:').free / psutil.disk_usage('C:').total) * 100:.1f}%")
    
    return detected_issues

if __name__ == "__main__":
    check_security_issues()
