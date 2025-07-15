#!/usr/bin/env python3
"""
Advanced Windows MCP Server - Complete PC Control
A comprehensive MCP server for full Windows system control
"""

import os
import subprocess
import sys
import platform
import json
import shutil
import time
import psutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
import ctypes
from ctypes import wintypes
import winreg

# Initialize FastMCP server
mcp = FastMCP("advanced-windows-control")

# ==============================================================================
# SYSTEM INFORMATION & MONITORING
# ==============================================================================

@mcp.tool()
async def get_system_info() -> str:
    """Get comprehensive Windows system information."""
    try:
        info = []
        info.append(f"System: {platform.system()} {platform.release()}")
        info.append(f"Version: {platform.version()}")
        info.append(f"Machine: {platform.machine()}")
        info.append(f"Processor: {platform.processor()}")
        info.append(f"Architecture: {platform.architecture()[0]}")
        info.append(f"User: {os.getenv('USERNAME', 'Unknown')}")
        info.append(f"Computer: {os.getenv('COMPUTERNAME', 'Unknown')}")
        info.append(f"Domain: {os.getenv('USERDOMAIN', 'Unknown')}")
        info.append(f"Current Directory: {os.getcwd()}")
        
        # Memory info
        memory = psutil.virtual_memory()
        info.append(f"Total RAM: {memory.total // (1024**3)} GB")
        info.append(f"Available RAM: {memory.available // (1024**3)} GB")
        info.append(f"RAM Usage: {memory.percent}%")
        
        # CPU info
        info.append(f"CPU Cores: {psutil.cpu_count()}")
        info.append(f"CPU Usage: {psutil.cpu_percent()}%")
        
        return "\\n".join(info)
    except Exception as e:
        return f"Error getting system info: {str(e)}"

@mcp.tool()
async def get_hardware_info() -> str:
    """Get detailed hardware information."""
    try:
        info = []
        
        # CPU details
        info.append("=== CPU Information ===")
        info.append(f"Logical CPUs: {psutil.cpu_count(logical=True)}")
        info.append(f"Physical CPUs: {psutil.cpu_count(logical=False)}")
        
        # Memory details
        info.append("\\n=== Memory Information ===")
        memory = psutil.virtual_memory()
        info.append(f"Total: {memory.total // (1024**3)} GB")
        info.append(f"Available: {memory.available // (1024**3)} GB")
        info.append(f"Used: {memory.used // (1024**3)} GB")
        info.append(f"Percentage: {memory.percent}%")
        
        # Disk information
        info.append("\\n=== Disk Information ===")
        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                info.append(f"Drive {partition.device}")
                info.append(f"  Total: {partition_usage.total // (1024**3)} GB")
                info.append(f"  Used: {partition_usage.used // (1024**3)} GB")
                info.append(f"  Free: {partition_usage.free // (1024**3)} GB")
            except:
                pass
        
        return "\\n".join(info)
    except Exception as e:
        return f"Error getting hardware info: {str(e)}"

# ==============================================================================
# PROCESS MANAGEMENT
# ==============================================================================

@mcp.tool()
async def list_processes() -> str:
    """List all running processes."""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(f"PID: {proc.info['pid']:<8} CPU: {proc.info['cpu_percent']:<6}% MEM: {proc.info['memory_percent']:<6.1f}% NAME: {proc.info['name']}")
            except:
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: float(x.split('CPU: ')[1].split('%')[0]), reverse=True)
        return "\\n".join(processes[:50])  # Top 50 processes
    except Exception as e:
        return f"Error listing processes: {str(e)}"

@mcp.tool()
async def kill_process(process_name_or_pid: str) -> str:
    """Kill a process by name or PID."""
    try:
        if process_name_or_pid.isdigit():
            # Kill by PID
            pid = int(process_name_or_pid)
            proc = psutil.Process(pid)
            proc.terminate()
            return f"Process with PID {pid} ({proc.name()}) terminated"
        else:
            # Kill by name
            killed = []
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == process_name_or_pid.lower():
                    proc.terminate()
                    killed.append(f"PID {proc.info['pid']}")
            
            if killed:
                return f"Terminated {process_name_or_pid}: {', '.join(killed)}"
            else:
                return f"No process found with name: {process_name_or_pid}"
    except Exception as e:
        return f"Error killing process: {str(e)}"

@mcp.tool()
async def start_process(executable_path: str, arguments: str = "") -> str:
    """Start a new process."""
    try:
        command = f'"{executable_path}" {arguments}' if arguments else executable_path
        process = subprocess.Popen(command, shell=True)
        return f"Started process: {executable_path} (PID: {process.pid})"
    except Exception as e:
        return f"Error starting process: {str(e)}"

# ==============================================================================
# FILE SYSTEM OPERATIONS
# ==============================================================================

@mcp.tool()
async def list_directory(path: str = ".", show_hidden: bool = False) -> str:
    """List directory contents with detailed information."""
    try:
        directory = Path(path)
        if not directory.exists():
            return f"Directory does not exist: {path}"
        
        if not directory.is_dir():
            return f"Path is not a directory: {path}"
        
        items = []
        for item in directory.iterdir():
            if not show_hidden and item.name.startswith('.'):
                continue
                
            try:
                stat = item.stat()
                size = stat.st_size
                modified = time.ctime(stat.st_mtime)
                
                if item.is_dir():
                    items.append(f"[DIR]  {item.name:<30} {modified}")
                else:
                    items.append(f"[FILE] {item.name:<30} {size:<12} bytes {modified}")
            except:
                items.append(f"[???]  {item.name:<30} (access denied)")
        
        return f"Directory: {path}\\n" + "\\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp.tool()
async def copy_file(source: str, destination: str) -> str:
    """Copy a file or directory."""
    try:
        source_path = Path(source)
        dest_path = Path(destination)
        
        if source_path.is_file():
            shutil.copy2(source, destination)
            return f"File copied: {source} -> {destination}"
        elif source_path.is_dir():
            shutil.copytree(source, destination)
            return f"Directory copied: {source} -> {destination}"
        else:
            return f"Source does not exist: {source}"
    except Exception as e:
        return f"Error copying: {str(e)}"

@mcp.tool()
async def move_file(source: str, destination: str) -> str:
    """Move a file or directory."""
    try:
        shutil.move(source, destination)
        return f"Moved: {source} -> {destination}"
    except Exception as e:
        return f"Error moving: {str(e)}"

@mcp.tool()
async def delete_file(path: str, force: bool = False) -> str:
    """Delete a file or directory."""
    try:
        file_path = Path(path)
        
        if not file_path.exists():
            return f"Path does not exist: {path}"
        
        if file_path.is_file():
            file_path.unlink()
            return f"File deleted: {path}"
        elif file_path.is_dir():
            if force:
                shutil.rmtree(path)
                return f"Directory deleted (forced): {path}"
            else:
                file_path.rmdir()
                return f"Directory deleted: {path}"
    except Exception as e:
        return f"Error deleting: {str(e)}"

@mcp.tool()
async def create_directory(path: str) -> str:
    """Create a new directory."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"Directory created: {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

@mcp.tool()
async def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """Read contents of a text file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"File does not exist: {file_path}"
        
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
        
        return f"File: {file_path}\\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def write_file(file_path: str, content: str, encoding: str = "utf-8") -> str:
    """Write content to a file."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return f"File written: {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# ==============================================================================
# NETWORK OPERATIONS
# ==============================================================================

@mcp.tool()
async def get_network_info() -> str:
    """Get network adapter information."""
    try:
        info = []
        info.append("=== Network Interfaces ===")
        
        for interface, addresses in psutil.net_if_addrs().items():
            info.append(f"\\nInterface: {interface}")
            for addr in addresses:
                if addr.family == 2:  # IPv4
                    info.append(f"  IPv4: {addr.address}")
                elif addr.family == 17:  # MAC
                    info.append(f"  MAC: {addr.address}")
        
        # Network stats
        info.append("\\n=== Network Statistics ===")
        net_stats = psutil.net_io_counters()
        info.append(f"Bytes Sent: {net_stats.bytes_sent}")
        info.append(f"Bytes Received: {net_stats.bytes_recv}")
        info.append(f"Packets Sent: {net_stats.packets_sent}")
        info.append(f"Packets Received: {net_stats.packets_recv}")
        
        return "\\n".join(info)
    except Exception as e:
        return f"Error getting network info: {str(e)}"

@mcp.tool()
async def ping_host(hostname: str, count: int = 4) -> str:
    """Ping a hostname or IP address."""
    try:
        result = subprocess.run(
            f"ping -n {count} {hostname}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return f"Ping {hostname}:\\n{result.stdout}"
    except Exception as e:
        return f"Error pinging {hostname}: {str(e)}"

@mcp.tool()
async def get_active_connections() -> str:
    """Get active network connections."""
    try:
        connections = []
        for conn in psutil.net_connections():
            if conn.status == 'ESTABLISHED':
                local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                connections.append(f"PID: {conn.pid:<8} {local:<25} -> {remote:<25} {conn.status}")
        
        return "Active Network Connections:\\n" + "\\n".join(connections[:50])
    except Exception as e:
        return f"Error getting connections: {str(e)}"

# ==============================================================================
# SYSTEM CONTROL
# ==============================================================================

@mcp.tool()
async def run_command(command: str) -> str:
    """Run a Windows command with enhanced safety checks."""
    try:
        # Enhanced safety checks
        dangerous_commands = [
            'format', 'fdisk', 'del /s', 'rmdir /s', 'rd /s',
            'shutdown /f', 'taskkill /f', 'reg delete', 'diskpart',
            'bcdedit', 'sfc /scannow', 'chkdsk /f'
        ]
        
        if any(danger in command.lower() for danger in dangerous_commands):
            return f"BLOCKED: Potentially dangerous command: {command}"
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\\nErrors: {result.stderr}"
            
        return f"Command: {command}\\nOutput: {output}"
    except subprocess.TimeoutExpired:
        return f"Command timed out: {command}"
    except Exception as e:
        return f"Error running command: {str(e)}"

@mcp.tool()
async def get_system_services() -> str:
    """Get Windows services status."""
    try:
        result = subprocess.run(
            'sc query state= all',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return f"Windows Services:\\n{result.stdout}"
    except Exception as e:
        return f"Error getting services: {str(e)}"

@mcp.tool()
async def control_service(service_name: str, action: str) -> str:
    """Control Windows service (start, stop, restart)."""
    try:
        if action.lower() not in ['start', 'stop', 'restart']:
            return "Invalid action. Use: start, stop, or restart"
        
        if action.lower() == 'restart':
            # Stop then start
            subprocess.run(f'net stop "{service_name}"', shell=True, capture_output=True)
            result = subprocess.run(f'net start "{service_name}"', shell=True, capture_output=True, text=True)
        else:
            command = f'net {action} "{service_name}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        return f"Service {service_name} {action}: {result.stdout}"
    except Exception as e:
        return f"Error controlling service: {str(e)}"

# ==============================================================================
# POWER MANAGEMENT
# ==============================================================================

@mcp.tool()
async def shutdown_system(delay_seconds: int = 0) -> str:
    """Shutdown the system."""
    try:
        command = f"shutdown /s /t {delay_seconds}"
        subprocess.run(command, shell=True)
        return f"System shutdown initiated (delay: {delay_seconds} seconds)"
    except Exception as e:
        return f"Error shutting down: {str(e)}"

@mcp.tool()
async def restart_system(delay_seconds: int = 0) -> str:
    """Restart the system."""
    try:
        command = f"shutdown /r /t {delay_seconds}"
        subprocess.run(command, shell=True)
        return f"System restart initiated (delay: {delay_seconds} seconds)"
    except Exception as e:
        return f"Error restarting: {str(e)}"

@mcp.tool()
async def cancel_shutdown() -> str:
    """Cancel a pending shutdown/restart."""
    try:
        subprocess.run("shutdown /a", shell=True)
        return "Shutdown/restart cancelled"
    except Exception as e:
        return f"Error cancelling shutdown: {str(e)}"

@mcp.tool()
async def sleep_system() -> str:
    """Put system to sleep."""
    try:
        subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
        return "System going to sleep"
    except Exception as e:
        return f"Error putting system to sleep: {str(e)}"

# ==============================================================================
# REGISTRY OPERATIONS
# ==============================================================================

@mcp.tool()
async def read_registry(key_path: str, value_name: str) -> str:
    """Read a value from Windows registry."""
    try:
        # Parse the key path
        if key_path.startswith("HKEY_LOCAL_MACHINE"):
            root = winreg.HKEY_LOCAL_MACHINE
            subkey = key_path.replace("HKEY_LOCAL_MACHINE\\\\", "")
        elif key_path.startswith("HKEY_CURRENT_USER"):
            root = winreg.HKEY_CURRENT_USER
            subkey = key_path.replace("HKEY_CURRENT_USER\\\\", "")
        else:
            return "Invalid registry path. Use HKEY_LOCAL_MACHINE or HKEY_CURRENT_USER"
        
        with winreg.OpenKey(root, subkey) as key:
            value, reg_type = winreg.QueryValueEx(key, value_name)
            return f"Registry value: {value} (Type: {reg_type})"
    except Exception as e:
        return f"Error reading registry: {str(e)}"

# ==============================================================================
# SYSTEM MONITORING
# ==============================================================================

@mcp.tool()
async def get_disk_usage(drive: str = "C:") -> str:
    """Get disk usage information."""
    try:
        total, used, free = shutil.disk_usage(drive)
        
        total_gb = total // (1024**3)
        used_gb = used // (1024**3)
        free_gb = free // (1024**3)
        usage_percent = (used / total) * 100
        
        return f"Disk Usage for {drive}\\n" + \
               f"Total: {total_gb} GB\\n" + \
               f"Used: {used_gb} GB ({usage_percent:.1f}%)\\n" + \
               f"Free: {free_gb} GB"
    except Exception as e:
        return f"Error getting disk usage: {str(e)}"

@mcp.tool()
async def get_environment_variables() -> str:
    """Get system environment variables."""
    try:
        important_vars = [
            'USERNAME', 'COMPUTERNAME', 'USERPROFILE', 'HOMEDRIVE', 'HOMEPATH',
            'WINDIR', 'SYSTEMROOT', 'TEMP', 'TMP', 'PATH', 'PROCESSOR_ARCHITECTURE',
            'PROCESSOR_IDENTIFIER', 'NUMBER_OF_PROCESSORS', 'OS', 'PATHEXT'
        ]
        
        vars_info = []
        for var in important_vars:
            value = os.getenv(var, 'Not Set')
            vars_info.append(f"{var}: {value}")
        
        return "Environment Variables:\\n" + "\\n".join(vars_info)
    except Exception as e:
        return f"Error getting environment variables: {str(e)}"

# ==============================================================================
# ADVANCED SYSTEM OPERATIONS
# ==============================================================================

@mcp.tool()
async def get_installed_programs() -> str:
    """Get list of installed programs."""
    try:
        programs = []
        
        # Check both 32-bit and 64-bit program entries
        registry_paths = [
            r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            r"SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
        ]
        
        for path in registry_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                    version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                                    programs.append(f"{name} - {version}")
                                except:
                                    pass
                        except:
                            pass
            except:
                pass
        
        programs.sort()
        return "Installed Programs:\\n" + "\\n".join(programs[:100])  # Top 100
    except Exception as e:
        return f"Error getting installed programs: {str(e)}"

@mcp.tool()
async def get_startup_programs() -> str:
    """Get programs that start with Windows."""
    try:
        startup_info = []
        
        # Registry startup locations
        startup_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")
        ]
        
        for root, path in startup_keys:
            try:
                with winreg.OpenKey(root, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_info.append(f"{name}: {value}")
                        except:
                            pass
            except:
                pass
        
        return "Startup Programs:\\n" + "\\n".join(startup_info)
    except Exception as e:
        return f"Error getting startup programs: {str(e)}"

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # Server runs silently when launched by Claude Desktop
    mcp.run()
