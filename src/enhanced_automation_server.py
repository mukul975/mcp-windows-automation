#!/usr/bin/env python3
"""
Enhanced Windows MCP Server with Automation & User Preferences
Complete PC control with smart automation and user preference management
"""

import os
import subprocess
import sys
import platform
import json
import shutil
import time
import psutil
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
import ctypes
from ctypes import wintypes
import winreg
import urllib.parse

# Initialize FastMCP server
mcp = FastMCP("enhanced-automation-control")

# User preferences storage
PREFERENCES_FILE = "user_preferences.json"

# ==============================================================================
# USER PREFERENCES MANAGEMENT
# ==============================================================================

def load_user_preferences() -> dict:
    """Load user preferences from file"""
    try:
        if Path(PREFERENCES_FILE).exists():
            with open(PREFERENCES_FILE, 'r') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_user_preferences(preferences: dict):
    """Save user preferences to file"""
    try:
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(preferences, f, indent=2)
    except Exception as e:
        print(f"Error saving preferences: {e}")

@mcp.tool()
async def set_user_preference(category: str, key: str, value: str) -> str:
    """Set a user preference (e.g., favorite song, default browser)"""
    try:
        preferences = load_user_preferences()
        
        if category not in preferences:
            preferences[category] = {}
        
        preferences[category][key] = value
        save_user_preferences(preferences)
        
        return f"Preference set: {category}.{key} = {value}"
    except Exception as e:
        return f"Error setting preference: {str(e)}"

@mcp.tool()
async def get_user_preference(category: str, key: str) -> str:
    """Get a user preference"""
    try:
        preferences = load_user_preferences()
        
        if category in preferences and key in preferences[category]:
            return f"{category}.{key} = {preferences[category][key]}"
        else:
            return f"Preference {category}.{key} not found"
    except Exception as e:
        return f"Error getting preference: {str(e)}"

@mcp.tool()
async def list_user_preferences() -> str:
    """List all user preferences"""
    try:
        preferences = load_user_preferences()
        
        if not preferences:
            return "No user preferences set"
        
        result = []
        for category, items in preferences.items():
            result.append(f"[{category}]")
            for key, value in items.items():
                result.append(f"  {key}: {value}")
            result.append("")
        
        return "User Preferences:\\n" + "\\n".join(result)
    except Exception as e:
        return f"Error listing preferences: {str(e)}"

# ==============================================================================
# SMART AUTOMATION TOOLS
# ==============================================================================

@mcp.tool()
async def open_youtube_with_search(search_query: str = "") -> str:
    """Open YouTube and search for a specific song/video"""
    try:
        if search_query:
            # URL encode the search query
            encoded_query = urllib.parse.quote(search_query)
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        else:
            youtube_url = "https://www.youtube.com"
        
        # Try to open with default browser first
        webbrowser.open(youtube_url)
        
        return f"Opened YouTube with search: '{search_query}'" if search_query else "Opened YouTube"
    except Exception as e:
        return f"Error opening YouTube: {str(e)}"

@mcp.tool()
async def play_favorite_song() -> str:
    """Play user's favorite song on YouTube"""
    try:
        preferences = load_user_preferences()
        
        if 'music' in preferences and 'favorite_song' in preferences['music']:
            favorite_song = preferences['music']['favorite_song']
            result = await open_youtube_with_search(favorite_song)
            return f"Playing your favorite song: {favorite_song}\\n{result}"
        else:
            return "No favorite song set. Use set_user_preference('music', 'favorite_song', 'Song Name') first"
    except Exception as e:
        return f"Error playing favorite song: {str(e)}"

@mcp.tool()
async def open_app_with_url(app_name: str, url: str = "") -> str:
    """Open an application with optional URL/parameters"""
    try:
        # Common application mappings
        app_mappings = {
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe'
        }
        
        executable = app_mappings.get(app_name.lower(), app_name)
        
        if url:
            command = f'"{executable}" "{url}"'
        else:
            command = executable
        
        process = subprocess.Popen(command, shell=True)
        return f"Opened {app_name} (PID: {process.pid})" + (f" with URL: {url}" if url else "")
    except Exception as e:
        return f"Error opening {app_name}: {str(e)}"

@mcp.tool()
async def smart_music_action(action: str = "play_favorite") -> str:
    """Smart music actions - play favorite, open music service, etc."""
    try:
        preferences = load_user_preferences()
        
        if action == "play_favorite":
            return await play_favorite_song()
        
        elif action == "open_spotify":
            return await open_app_with_url("spotify")
        
        elif action == "open_youtube_music":
            return await open_app_with_url("chrome", "https://music.youtube.com")
        
        elif action == "open_pandora":
            return await open_app_with_url("chrome", "https://www.pandora.com")
        
        elif action == "random_song":
            # Get random song from user's playlist if available
            if 'music' in preferences and 'playlist' in preferences['music']:
                import random
                playlist = preferences['music']['playlist']
                if isinstance(playlist, list) and playlist:
                    random_song = random.choice(playlist)
                    return await open_youtube_with_search(random_song)
            return "No playlist found. Add songs to your playlist first."
        
        else:
            return f"Unknown music action: {action}. Available: play_favorite, open_spotify, open_youtube_music, open_pandora, random_song"
    
    except Exception as e:
        return f"Error with music action: {str(e)}"

@mcp.tool()
async def add_to_playlist(song_name: str) -> str:
    """Add a song to user's playlist"""
    try:
        preferences = load_user_preferences()
        
        if 'music' not in preferences:
            preferences['music'] = {}
        
        if 'playlist' not in preferences['music']:
            preferences['music']['playlist'] = []
        
        if song_name not in preferences['music']['playlist']:
            preferences['music']['playlist'].append(song_name)
            save_user_preferences(preferences)
            return f"Added '{song_name}' to your playlist"
        else:
            return f"'{song_name}' is already in your playlist"
    
    except Exception as e:
        return f"Error adding to playlist: {str(e)}"

@mcp.tool()
async def show_playlist() -> str:
    """Show user's current playlist"""
    try:
        preferences = load_user_preferences()
        
        if 'music' in preferences and 'playlist' in preferences['music']:
            playlist = preferences['music']['playlist']
            if playlist:
                return "Your Playlist:\\n" + "\\n".join(f"{i+1}. {song}" for i, song in enumerate(playlist))
            else:
                return "Your playlist is empty"
        else:
            return "No playlist found"
    
    except Exception as e:
        return f"Error showing playlist: {str(e)}"

# ==============================================================================
# ENHANCED AUTOMATION COMMANDS
# ==============================================================================

@mcp.tool()
async def smart_open_command(app_or_service: str, additional_params: str = "") -> str:
    """Smart command to open applications, websites, or services with context"""
    try:
        app_lower = app_or_service.lower()
        
        # Music services
        if "youtube" in app_lower:
            if "music" in additional_params.lower():
                return await open_app_with_url("chrome", "https://music.youtube.com")
            elif additional_params:
                return await open_youtube_with_search(additional_params)
            else:
                return await open_app_with_url("chrome", "https://www.youtube.com")
        
        elif "spotify" in app_lower:
            return await open_app_with_url("spotify")
        
        elif "music" in app_lower:
            return await smart_music_action("play_favorite")
        
        # Browsers
        elif app_lower in ["chrome", "firefox", "edge"]:
            return await open_app_with_url(app_lower, additional_params)
        
        # Common applications
        elif app_lower in ["notepad", "calculator", "explorer", "cmd", "powershell"]:
            return await open_app_with_url(app_lower, additional_params)
        
        # Social media
        elif "facebook" in app_lower:
            return await open_app_with_url("chrome", "https://www.facebook.com")
        
        elif "twitter" in app_lower:
            return await open_app_with_url("chrome", "https://www.twitter.com")
        
        elif "instagram" in app_lower:
            return await open_app_with_url("chrome", "https://www.instagram.com")
        
        # Default: try to open as application
        else:
            return await open_app_with_url(app_or_service, additional_params)
    
    except Exception as e:
        return f"Error with smart open command: {str(e)}"

@mcp.tool()
async def quick_setup_favorites() -> str:
    """Quick setup for common user favorites"""
    try:
        setup_guide = """
Quick Setup Guide for Favorites:

1. Set your favorite song:
   set_user_preference('music', 'favorite_song', 'Your Song Name')

2. Set your default browser:
   set_user_preference('apps', 'browser', 'chrome')

3. Add songs to playlist:
   add_to_playlist('Song Name 1')
   add_to_playlist('Song Name 2')

4. Set favorite websites:
   set_user_preference('web', 'news', 'https://news.google.com')
   set_user_preference('web', 'social', 'https://facebook.com')

Example usage after setup:
- "Play my favorite song" -> play_favorite_song()
- "Open YouTube with my favorite song" -> Uses your preference
- "Play random song from playlist" -> smart_music_action('random_song')
"""
        return setup_guide
    except Exception as e:
        return f"Error showing setup guide: {str(e)}"

# ==============================================================================
# INCLUDE ALL PREVIOUS ADVANCED TOOLS
# ==============================================================================

# Copy all the previous tools from advanced_windows_control_server.py
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

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # Server runs silently when launched by Claude Desktop
    mcp.run()
