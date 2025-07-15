#!/usr/bin/env python3
"""
Simple Windows MCP Server
A streamlined MCP server for basic Windows operations
"""

import os
import subprocess
import sys
import platform
import json
from pathlib import Path
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("simple-windows-server")

@mcp.tool()
async def get_system_info() -> str:
    """Get basic Windows system information."""
    try:
        info = []
        info.append(f"System: {platform.system()} {platform.release()}")
        info.append(f"Machine: {platform.machine()}")
        info.append(f"Processor: {platform.processor()}")
        info.append(f"User: {os.getenv('USERNAME', 'Unknown')}")
        info.append(f"Computer: {os.getenv('COMPUTERNAME', 'Unknown')}")
        info.append(f"Current Directory: {os.getcwd()}")
        
        return "\\n".join(info)
    except Exception as e:
        return f"Error getting system info: {str(e)}"

@mcp.tool()
async def run_command(command: str) -> str:
    """Run a Windows command safely."""
    try:
        # Basic safety check
        dangerous_commands = ['format', 'fdisk', 'del /s', 'rmdir /s', 'shutdown', 'restart']
        if any(danger in command.lower() for danger in dangerous_commands):
            return f"ERROR: Dangerous command blocked: {command}"
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
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
async def list_directory(path: str = ".") -> str:
    """List contents of a directory."""
    try:
        directory = Path(path)
        if not directory.exists():
            return f"Directory does not exist: {path}"
        
        if not directory.is_dir():
            return f"Path is not a directory: {path}"
        
        items = []
        for item in directory.iterdir():
            if item.is_dir():
                items.append(f"[DIR] {item.name}/")
            else:
                size = item.stat().st_size
                items.append(f"[FILE] {item.name} ({size} bytes)")
        
        return f"Directory: {path}\\n" + "\\n".join(items)
        
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp.tool()
async def read_file(file_path: str) -> str:
    """Read contents of a text file."""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"File does not exist: {file_path}"
        
        if not path.is_file():
            return f"Path is not a file: {file_path}"
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"File: {file_path}\\n{content}"
        
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def write_file(file_path: str, content: str) -> str:
    """Write content to a file."""
    try:
        path = Path(file_path)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"File written successfully: {file_path}"
        
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
async def get_environment_variables() -> str:
    """Get Windows environment variables."""
    try:
        important_vars = [
            'USERNAME', 'COMPUTERNAME', 'USERPROFILE', 'HOMEDRIVE', 'HOMEPATH',
            'WINDIR', 'SYSTEMROOT', 'TEMP', 'TMP', 'PATH'
        ]
        
        vars_info = []
        for var in important_vars:
            value = os.getenv(var, 'Not Set')
            vars_info.append(f"{var}: {value}")
        
        return "Environment Variables:\\n" + "\\n".join(vars_info)
        
    except Exception as e:
        return f"Error getting environment variables: {str(e)}"

@mcp.tool()
async def ping_host(hostname: str) -> str:
    """Ping a hostname or IP address."""
    try:
        result = subprocess.run(
            f"ping -n 4 {hostname}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        return f"Ping {hostname}:\\n{result.stdout}"
        
    except subprocess.TimeoutExpired:
        return f"Ping timeout for {hostname}"
    except Exception as e:
        return f"Error pinging {hostname}: {str(e)}"

@mcp.tool()
async def get_disk_usage(drive: str = "C:") -> str:
    """Get disk usage information for a drive."""
    try:
        import shutil
        
        total, used, free = shutil.disk_usage(drive)
        
        # Convert to GB
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

if __name__ == "__main__":
    # Don't modify stdout/stderr as it interferes with MCP stdio
    # The server will run silently when launched by Claude Desktop
    mcp.run()
