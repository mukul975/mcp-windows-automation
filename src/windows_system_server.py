import os
import subprocess
import sys
import json
import shutil
import winreg
from typing import Any, Dict, List
from pathlib import Path
import asyncio
import psutil
import time
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("windows-system-control")

# Security whitelist for safe commands
SAFE_COMMANDS = {
    'file_operations': ['dir', 'type', 'copy', 'move', 'del', 'mkdir', 'rmdir'],
    'system_info': ['systeminfo', 'tasklist', 'ipconfig', 'ping', 'netstat'],
    'process_control': ['tasklist', 'taskkill'],
    'network': ['ping', 'nslookup', 'ipconfig', 'netstat'],
    'service_control': ['sc', 'net']
}

# Dangerous commands that require explicit confirmation
DANGEROUS_COMMANDS = ['format', 'fdisk', 'del', 'rmdir', 'shutdown', 'restart']

@mcp.tool()
async def execute_command(command: str, confirm_dangerous: bool = False) -> str:
    """Execute a Windows command with safety checks.
    
    Args:
        command: The command to execute
        confirm_dangerous: Set to True to confirm execution of potentially dangerous commands
    """
    try:
        # Check for dangerous commands
        cmd_lower = command.lower()
        if any(dangerous in cmd_lower for dangerous in DANGEROUS_COMMANDS):
            if not confirm_dangerous:
                return f"⚠️ DANGEROUS COMMAND DETECTED: '{command}'\nThis command could be harmful. If you're sure you want to execute it, call this tool again with confirm_dangerous=True"
        
        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nErrors: {result.stderr}"
            
        return f"✅ Command executed successfully:\n{output}"
        
    except subprocess.TimeoutExpired:
        return "❌ Command timed out after 30 seconds"
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"

@mcp.tool()
async def file_operations(action: str, source: str, destination: str = None) -> str:
    """Perform file operations like copy, move, delete, create directory.
    
    Args:
        action: Operation to perform (copy, move, delete, create_dir, read, write)
        source: Source file or directory path
        destination: Destination path (required for copy/move)
    """
    try:
        source_path = Path(source)
        
        if action == "read":
            if source_path.exists() and source_path.is_file():
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"📄 File content:\n{content}"
            else:
                return f"❌ File not found: {source}"
                
        elif action == "write":
            if not destination:
                return "❌ Destination content required for write operation"
            with open(source_path, 'w', encoding='utf-8') as f:
                f.write(destination)
            return f"✅ File written successfully: {source}"
            
        elif action == "copy":
            if not destination:
                return "❌ Destination required for copy operation"
            shutil.copy2(source, destination)
            return f"✅ File copied from {source} to {destination}"
            
        elif action == "move":
            if not destination:
                return "❌ Destination required for move operation"
            shutil.move(source, destination)
            return f"✅ File moved from {source} to {destination}"
            
        elif action == "delete":
            if source_path.is_file():
                source_path.unlink()
                return f"✅ File deleted: {source}"
            elif source_path.is_dir():
                shutil.rmtree(source)
                return f"✅ Directory deleted: {source}"
            else:
                return f"❌ Path not found: {source}"
                
        elif action == "create_dir":
            source_path.mkdir(parents=True, exist_ok=True)
            return f"✅ Directory created: {source}"
            
        else:
            return f"❌ Unknown action: {action}"
            
    except Exception as e:
        return f"❌ Error performing file operation: {str(e)}"

@mcp.tool()
async def system_info() -> str:
    """Get comprehensive system information."""
    try:
        # Basic system info
        import platform
        info = []
        info.append(f"🖥️ System: {platform.system()} {platform.release()}")
        info.append(f"💻 Machine: {platform.machine()}")
        info.append(f"🔧 Processor: {platform.processor()}")
        
        # Memory info
        memory = psutil.virtual_memory()
        info.append(f"💾 Total Memory: {memory.total // (1024**3)} GB")
        info.append(f"📊 Available Memory: {memory.available // (1024**3)} GB")
        info.append(f"⚡ Memory Usage: {memory.percent}%")
        
        # Disk info
        disk = psutil.disk_usage('C:\\')
        info.append(f"💿 Total Disk Space: {disk.total // (1024**3)} GB")
        info.append(f"📂 Free Disk Space: {disk.free // (1024**3)} GB")
        info.append(f"📈 Disk Usage: {(disk.used / disk.total) * 100:.1f}%")
        
        # CPU info
        info.append(f"🔥 CPU Usage: {psutil.cpu_percent(interval=1)}%")
        info.append(f"⚙️ CPU Cores: {psutil.cpu_count()}")
        
        return "\n".join(info)
        
    except Exception as e:
        return f"❌ Error getting system info: {str(e)}"

@mcp.tool()
async def process_management(action: str, process_name: str = None, pid: int = None) -> str:
    """Manage system processes.
    
    Args:
        action: Action to perform (list, kill, info)
        process_name: Name of the process (for kill/info actions)
        pid: Process ID (alternative to process_name)
    """
    try:
        if action == "list":
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU: {proc.info['cpu_percent']:.1f}%, Memory: {proc.info['memory_percent']:.1f}%")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Show top 20 processes
            return "🔍 Running Processes (Top 20):\n" + "\n".join(processes[:20])
            
        elif action == "kill":
            if not process_name and not pid:
                return "❌ Process name or PID required for kill action"
                
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if (process_name and proc.info['name'].lower() == process_name.lower()) or \
                       (pid and proc.info['pid'] == pid):
                        proc.kill()
                        killed = True
                        return f"✅ Process killed: {proc.info['name']} (PID: {proc.info['pid']})"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            if not killed:
                return f"❌ Process not found: {process_name or pid}"
                
        elif action == "info":
            if not process_name and not pid:
                return "❌ Process name or PID required for info action"
                
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    if (process_name and proc.info['name'].lower() == process_name.lower()) or \
                       (pid and proc.info['pid'] == pid):
                        return f"📊 Process Info:\nPID: {proc.info['pid']}\nName: {proc.info['name']}\nStatus: {proc.info['status']}\nCPU: {proc.info['cpu_percent']:.1f}%\nMemory: {proc.info['memory_percent']:.1f}%"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return f"❌ Process not found: {process_name or pid}"
            
        else:
            return f"❌ Unknown action: {action}"
            
    except Exception as e:
        return f"❌ Error managing process: {str(e)}"

@mcp.tool()
async def network_operations(action: str, target: str = None) -> str:
    """Perform network operations.
    
    Args:
        action: Operation to perform (ping, ipconfig, netstat, nslookup)
        target: Target for operations like ping or nslookup
    """
    try:
        if action == "ping":
            if not target:
                return "❌ Target required for ping operation"
            result = subprocess.run(f"ping -n 4 {target}", shell=True, capture_output=True, text=True)
            return f"🌐 Ping Results:\n{result.stdout}"
            
        elif action == "ipconfig":
            result = subprocess.run("ipconfig /all", shell=True, capture_output=True, text=True)
            return f"🔧 IP Configuration:\n{result.stdout}"
            
        elif action == "netstat":
            result = subprocess.run("netstat -an", shell=True, capture_output=True, text=True)
            return f"📡 Network Connections:\n{result.stdout[:2000]}..."  # Truncate for readability
            
        elif action == "nslookup":
            if not target:
                return "❌ Target required for nslookup operation"
            result = subprocess.run(f"nslookup {target}", shell=True, capture_output=True, text=True)
            return f"🔍 DNS Lookup Results:\n{result.stdout}"
            
        else:
            return f"❌ Unknown network action: {action}"
            
    except Exception as e:
        return f"❌ Error performing network operation: {str(e)}"

@mcp.tool()
async def application_control(action: str, app_name: str = None, app_path: str = None) -> str:
    """Control applications (start, stop, find).
    
    Args:
        action: Action to perform (start, stop, find)
        app_name: Name of the application
        app_path: Full path to the application executable
    """
    try:
        if action == "start":
            if not app_name and not app_path:
                return "❌ Application name or path required"
                
            if app_path:
                subprocess.Popen(app_path)
                return f"✅ Application started: {app_path}"
            else:
                subprocess.Popen(app_name, shell=True)
                return f"✅ Application started: {app_name}"
                
        elif action == "stop":
            if not app_name:
                return "❌ Application name required for stop action"
                
            result = subprocess.run(f"taskkill /f /im {app_name}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return f"✅ Application stopped: {app_name}"
            else:
                return f"❌ Failed to stop application: {app_name}\n{result.stderr}"
                
        elif action == "find":
            if not app_name:
                return "❌ Application name required for find action"
                
            result = subprocess.run(f"where {app_name}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return f"📍 Application found at: {result.stdout.strip()}"
            else:
                return f"❌ Application not found: {app_name}"
                
        else:
            return f"❌ Unknown action: {action}"
            
    except Exception as e:
        return f"❌ Error controlling application: {str(e)}"

@mcp.tool()
async def registry_operations(action: str, key_path: str, value_name: str = None, value_data: str = None) -> str:
    """Perform Windows registry operations (read only for safety).
    
    Args:
        action: Operation to perform (read, list_keys, list_values)
        key_path: Registry key path (e.g., "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion")
        value_name: Name of the registry value
        value_data: Data to write (not implemented for safety)
    """
    try:
        # Parse the key path
        key_parts = key_path.split('\\', 1)
        if len(key_parts) != 2:
            return "❌ Invalid key path format"
            
        root_key_name = key_parts[0]
        sub_key_path = key_parts[1]
        
        # Map root key names to constants
        root_keys = {
            'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE,
            'HKEY_CURRENT_USER': winreg.HKEY_CURRENT_USER,
            'HKEY_CLASSES_ROOT': winreg.HKEY_CLASSES_ROOT,
            'HKEY_USERS': winreg.HKEY_USERS,
            'HKEY_CURRENT_CONFIG': winreg.HKEY_CURRENT_CONFIG,
        }
        
        if root_key_name not in root_keys:
            return f"❌ Invalid root key: {root_key_name}"
            
        root_key = root_keys[root_key_name]
        
        if action == "read":
            if not value_name:
                return "❌ Value name required for read operation"
                
            with winreg.OpenKey(root_key, sub_key_path, 0, winreg.KEY_READ) as key:
                value, reg_type = winreg.QueryValueEx(key, value_name)
                return f"📖 Registry Value:\nPath: {key_path}\nValue: {value_name}\nData: {value}\nType: {reg_type}"
                
        elif action == "list_keys":
            keys = []
            with winreg.OpenKey(root_key, sub_key_path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        keys.append(subkey_name)
                        i += 1
                    except OSError:
                        break
            return f"📂 Registry Subkeys in {key_path}:\n" + "\n".join(keys[:50])  # Limit output
            
        elif action == "list_values":
            values = []
            with winreg.OpenKey(root_key, sub_key_path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        value_name, value_data, reg_type = winreg.EnumValue(key, i)
                        values.append(f"{value_name}: {value_data} (Type: {reg_type})")
                        i += 1
                    except OSError:
                        break
            return f"📋 Registry Values in {key_path}:\n" + "\n".join(values[:50])  # Limit output
            
        else:
            return f"❌ Unknown registry action: {action}"
            
    except Exception as e:
        return f"❌ Error performing registry operation: {str(e)}"

@mcp.tool()
async def system_control(action: str, delay: int = 0) -> str:
    """Control system power states (shutdown, restart, sleep).
    
    Args:
        action: Action to perform (shutdown, restart, sleep, cancel)
        delay: Delay in seconds before action (default: 0)
    """
    try:
        if action == "shutdown":
            if delay > 0:
                subprocess.run(f"shutdown /s /t {delay}", shell=True)
                return f"⏰ System will shutdown in {delay} seconds"
            else:
                subprocess.run("shutdown /s /t 0", shell=True)
                return "🔌 System is shutting down now"
                
        elif action == "restart":
            if delay > 0:
                subprocess.run(f"shutdown /r /t {delay}", shell=True)
                return f"⏰ System will restart in {delay} seconds"
            else:
                subprocess.run("shutdown /r /t 0", shell=True)
                return "🔄 System is restarting now"
                
        elif action == "sleep":
            subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
            return "😴 System is going to sleep"
            
        elif action == "cancel":
            subprocess.run("shutdown /a", shell=True)
            return "❌ Shutdown/restart cancelled"
            
        else:
            return f"❌ Unknown system control action: {action}"
            
    except Exception as e:
        return f"❌ Error controlling system: {str(e)}"

if __name__ == "__main__":
    print("🚀 Starting Windows System Control MCP Server...")
    print("📝 Available tools:")
    print("   - execute_command: Execute Windows commands")
    print("   - file_operations: File and directory operations")
    print("   - system_info: Get system information")
    print("   - process_management: Manage processes")
    print("   - network_operations: Network utilities")
    print("   - application_control: Start/stop applications")
    print("   - registry_operations: Read registry values")
    print("   - system_control: Shutdown/restart/sleep")
    print("⚠️  Remember to configure this server in Claude Desktop!")
    
    mcp.run(transport='stdio')
