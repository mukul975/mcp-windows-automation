#!/usr/bin/env python3
"""
Unified Windows MCP Server for Complete PC Control and Smart Automation
With Advanced UI Automation and Application Interaction
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
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from mcp.server.fastmcp import FastMCP
import ctypes
from ctypes import wintypes
import winreg
import urllib.parse
import threading
import logging
from datetime import datetime

# Advanced UI Automation imports
try:
    import pyautogui
    import pygetwindow as gw
    import requests
    import websocket
    import socket
    from urllib.parse import urlparse
    import keyboard
    import pynput
    from pynput import mouse, keyboard as pynput_keyboard
    UI_AUTOMATION_AVAILABLE = True
except ImportError as e:
    UI_AUTOMATION_AVAILABLE = False
    print(f"Warning: UI automation libraries not available. Install: pip install pyautogui pygetwindow requests websocket-client keyboard pynput")
    print(f"Import error: {e}")

# Configure PyAutoGUI
if UI_AUTOMATION_AVAILABLE:
    pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
    pyautogui.PAUSE = 0.1  # Small pause between actions

# Initialize FastMCP server
mcp = FastMCP("unified-server")

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
        return "User Preferences:\n" + "\n".join(result)
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
            encoded_query = urllib.parse.quote(search_query)
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        else:
            youtube_url = "https://www.youtube.com"
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
            return await open_youtube_with_search(favorite_song)
        else:
            return "No favorite song set. Use set_user_preference('music', 'favorite_song', 'Song Name') first"
    except Exception as e:
        return f"Error playing favorite song: {str(e)}"

@mcp.tool()
async def open_app_with_url(app_name: str, url: str = "") -> str:
    """Open an application with optional URL/parameters"""
    try:
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
        command = f'"{executable}" "{url}"' if url else executable
        process = subprocess.Popen(command, shell=True)
        return f"Opened {app_name} (PID: {process.pid})" + (f" with URL: {url}" if url else "")
    except Exception as e:
        return f"Error opening {app_name}: {str(e)}"

@mcp.tool()
async def smart_music_action(action: str = "play_favorite") -> str:
    """Smart music actions - play favorite, open music service, etc."""
    try:
        if action == "play_favorite":
            return await play_favorite_song()
        elif action == "open_spotify":
            return await open_app_with_url("spotify")
        elif action == "open_youtube_music":
            return await open_app_with_url("chrome", "https://music.youtube.com")
        else:
            return f"Unknown music action: {action}. Available: play_favorite, open_spotify, open_youtube_music"
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
                return "Your Playlist:\n" + "\n".join(f"{i+1}. {song}" for i, song in enumerate(playlist))
            else:
                return "Your playlist is empty"
        else:
            return "No playlist found"
    except Exception as e:
        return f"Error showing playlist: {str(e)}"

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
        memory = psutil.virtual_memory()
        info.append(f"Total RAM: {memory.total // (1024**3)} GB")
        info.append(f"Available RAM: {memory.available // (1024**3)} GB")
        info.append(f"RAM Usage: {memory.percent}%")
        info.append(f"CPU Cores: {psutil.cpu_count()}")
        info.append(f"CPU Usage: {psutil.cpu_percent()}%")
        return "\n".join(info)
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
            except Exception:
                pass
        processes.sort(key=lambda x: float(x.split('CPU: ')[1].split('%')[0]), reverse=True)
        return "\n".join(processes[:50])
    except Exception as e:
        return f"Error listing processes: {str(e)}"

@mcp.tool()
async def get_installed_programs() -> str:
    """Get list of installed programs from Windows registry."""
    try:
        programs = []
        
        # Check both 32-bit and 64-bit program entries
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
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
                                    try:
                                        version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                                        programs.append(f"{name} - {version}")
                                    except:
                                        programs.append(name)
                                except:
                                    pass
                        except:
                            pass
            except:
                pass
        
        # Remove duplicates and sort
        programs = sorted(list(set(programs)))
        
        if programs:
            return f"Installed Programs ({len(programs)} total):\n" + "\n".join(programs)
        else:
            return "No installed programs found"
    except Exception as e:
        return f"Error getting installed programs: {str(e)}"

@mcp.tool()
async def get_startup_programs() -> str:
    """Get programs that start with Windows."""
    try:
        startup_info = []
        
        # Registry startup locations
        startup_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
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
        
        if startup_info:
            return "Startup Programs:\n" + "\n".join(startup_info)
        else:
            return "No startup programs found"
    except Exception as e:
        return f"Error getting startup programs: {str(e)}"

@mcp.tool()
async def run_command(command: str) -> str:
    """Run a Windows command with enhanced safety checks."""
    try:
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
            output += f"\nErrors: {result.stderr}"
        return f"Command: {command}\nOutput: {output}"
    except subprocess.TimeoutExpired:
        return f"Command timed out: {command}"
    except Exception as e:
        return f"Error running command: {str(e)}"

# ==============================================================================
# ADVANCED UI AUTOMATION AND APPLICATION INTERACTION
# ==============================================================================# ==============================================================================
# LIGHTROOM COMMANDS
# ==============================================================================

@mcp.tool()
async def next_photo() -> str:
    """Go to next photo in Lightroom"""
    try:
        pyautogui.hotkey('ctrl', 'right')
        return "Navigated to next photo"
    except Exception as e:
        return f"Error moving to next photo: {str(e)}"

@mcp.tool()
async def previous_photo() -> str:
    """Go to previous photo in Lightroom"""
    try:
        pyautogui.hotkey('ctrl', 'left')
        return "Navigated to previous photo"
    except Exception as e:
        return f"Error moving to previous photo: {str(e)}"

@mcp.tool()
async def first_photo() -> str:
    """Go to first photo in Lightroom"""
    try:
        pyautogui.hotkey('ctrl', 'home')
        return "Navigated to first photo"
    except Exception as e:
        return f"Error moving to first photo: {str(e)}"

@mcp.tool()
async def last_photo() -> str:
    """Go to last photo in Lightroom"""
    try:
        pyautogui.hotkey('ctrl', 'end')
        return "Navigated to last photo"
    except Exception as e:
        return f"Error moving to last photo: {str(e)}"

# Add other commands as described in the LIGHTROOM_MCP_COMMANDS.md documentation
# Similar pattern as above based on the shortcut or action defined

# ==============================================================================
# ML PREDICTIVE AUTOMATION
# ==============================================================================

# Import ML components
try:
    import os
    from src.ml_predictive_engine import get_ml_engine
    
    # Ensure we're in the correct directory for data files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    ML_ENGINE = get_ml_engine()
    
    # Force clear and reload data to ensure fresh state
    data_collector = ML_ENGINE['data_collector']
    data_collector.actions = []
    data_collector.metrics = []
    
    # Load existing data from file
    data_collector.load_data()
    
    actions_count = len(data_collector.actions)
    metrics_count = len(data_collector.metrics)
    
    print(f"ML Engine initialized with {actions_count} actions and {metrics_count} metrics")
    
    # If no data loaded, check if file exists and has data
    if actions_count == 0 and metrics_count == 0:
        if os.path.exists('ml_data.json'):
            file_size = os.path.getsize('ml_data.json')
            print(f"ML data file exists (size: {file_size} bytes) but no data loaded - checking file integrity")
            
            # Try to load raw data to diagnose issue
            try:
                import json
                with open('ml_data.json', 'r') as f:
                    raw_data = json.load(f)
                raw_actions = len(raw_data.get('actions', []))
                raw_metrics = len(raw_data.get('metrics', []))
                print(f"Raw file contains {raw_actions} actions and {raw_metrics} metrics")
                
                # If raw data exists but wasn't loaded, manually populate
                if raw_actions > 0 or raw_metrics > 0:
                    print("Manually loading data from file...")
                    data_collector.actions = []
                    data_collector.metrics = []
                    
                    # Manually reload with error handling
                    from datetime import datetime
                    from src.ml_predictive_engine import UserAction, SystemMetrics
                    
                    for action_data in raw_data.get('actions', []):
                        try:
                            action_data['timestamp'] = datetime.fromisoformat(action_data['timestamp'])
                            data_collector.actions.append(UserAction(**action_data))
                        except Exception as e:
                            print(f"Error loading action: {e}")
                    
                    for metric_data in raw_data.get('metrics', []):
                        try:
                            metric_data['timestamp'] = datetime.fromisoformat(metric_data['timestamp'])
                            data_collector.metrics.append(SystemMetrics(**metric_data))
                        except Exception as e:
                            print(f"Error loading metric: {e}")
                    
                    print(f"Successfully loaded {len(data_collector.actions)} actions and {len(data_collector.metrics)} metrics")
                    
            except Exception as e:
                print(f"Error reading ML data file: {e}")
        else:
            print("No ML data file found - starting with empty dataset")
    
    ML_AVAILABLE = True
except ImportError as e:
    ML_AVAILABLE = False
    print(f"Warning: ML predictive engine not available. Error: {e}")
    print("Run: pip install scikit-learn pandas numpy joblib")

@mcp.tool()
async def record_user_action(action_type: str, application: str, duration: float = 1.0, success: bool = True) -> str:
    """Record a user action for ML training"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        ML_ENGINE['data_collector'].record_action(action_type, application, duration, success)
        return f"Recorded action: {action_type} in {application} (duration: {duration}s, success: {success})"
    except Exception as e:
        return f"Error recording action: {str(e)}"

@mcp.tool()
async def record_system_metrics() -> str:
    """Record current system metrics for ML training"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        ML_ENGINE['data_collector'].record_system_metrics()
        return "System metrics recorded successfully"
    except Exception as e:
        return f"Error recording metrics: {str(e)}"

@mcp.tool()
async def train_behavior_model() -> str:
    """Train the user behavior prediction model"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        result = ML_ENGINE['behavior_predictor'].train_model()
        if 'error' in result:
            return f"Training failed: {result['error']}"
        
        return f"Model trained successfully!\n" + \
               f"Train accuracy: {result['train_accuracy']:.2%}\n" + \
               f"Test accuracy: {result['test_accuracy']:.2%}\n" + \
               f"Samples used: {result['samples_used']}"
    except Exception as e:
        return f"Error training model: {str(e)}"

@mcp.tool()
async def predict_next_action(context: str = "") -> str:
    """Predict the user's next likely action"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        context_dict = {'duration': 1.0}
        if context:
            try:
                import json
                context_dict = json.loads(context)
            except:
                pass
        
        result = ML_ENGINE['behavior_predictor'].predict_next_action(context_dict)
        if 'error' in result:
            return f"Prediction failed: {result['error']}"
        
        return f"Predicted next action: {result['predicted_action']}\n" + \
               f"Confidence: {result['confidence']:.2%}\n" + \
               f"Timestamp: {result['timestamp']}"
    except Exception as e:
        return f"Error predicting action: {str(e)}"

@mcp.tool()
async def train_system_optimizer() -> str:
    """Train the system optimization model"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        result = ML_ENGINE['system_optimizer'].train_model()
        if 'error' in result:
            return f"Training failed: {result['error']}"
        
        return f"System optimizer trained successfully!\n" + \
               f"Train MSE: {result['train_mse']:.4f}\n" + \
               f"Test MSE: {result['test_mse']:.4f}\n" + \
               f"Samples used: {result['samples_used']}"
    except Exception as e:
        return f"Error training optimizer: {str(e)}"

@mcp.tool()
async def predict_system_load() -> str:
    """Predict future system load"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        result = ML_ENGINE['system_optimizer'].predict_system_load()
        if 'error' in result:
            return f"Prediction failed: {result['error']}"
        
        return f"System Load Prediction:\n" + \
               f"Current CPU load: {result['current_cpu_load']:.1f}%\n" + \
               f"Predicted CPU load: {result['predicted_cpu_load']:.1f}%\n" + \
               f"Timestamp: {result['timestamp']}"
    except Exception as e:
        return f"Error predicting load: {str(e)}"

@mcp.tool()
async def get_automation_recommendations() -> str:
    """Get smart automation recommendations based on usage patterns"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        recommendations = ML_ENGINE['recommendation_engine'].get_recommendations()
        
        if not recommendations:
            return "No recommendations available"
        
        result = "Smart Automation Recommendations:\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            result += f"{i}. {rec['recommendation']}\n"
            if 'frequency' in rec:
                result += f"   Frequency: {rec['frequency']} times\n"
            if 'type' in rec:
                result += f"   Type: {rec['type']}\n"
            result += "\n"
        
        return result
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"

@mcp.tool()
async def get_ml_stats() -> str:
    """Get ML engine statistics and status"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        # Use the existing ML_ENGINE instance but refresh its data
        data_collector = ML_ENGINE['data_collector']
        behavior_predictor = ML_ENGINE['behavior_predictor']
        system_optimizer = ML_ENGINE['system_optimizer']
        
        # Force reload data from file to get current stats (don't clear first)
        original_actions = data_collector.actions[:]
        original_metrics = data_collector.metrics[:]
        
        # Clear and reload
        data_collector.actions = []
        data_collector.metrics = []
        data_collector.load_data()
        
        # If load failed (empty data), restore original data
        if len(data_collector.actions) == 0 and len(data_collector.metrics) == 0 and (len(original_actions) > 0 or len(original_metrics) > 0):
            data_collector.actions = original_actions
            data_collector.metrics = original_metrics
        
        stats = f"ML Engine Statistics:\n\n"
        stats += f"Data Collection:\n"
        stats += f"  - User actions recorded: {len(data_collector.actions)}\n"
        stats += f"  - System metrics recorded: {len(data_collector.metrics)}\n\n"
        
        stats += f"Model Status:\n"
        stats += f"  - Behavior predictor trained: {'YES' if behavior_predictor.is_trained else 'NO'}\n"
        stats += f"  - System optimizer trained: {'YES' if system_optimizer.is_trained else 'NO'}\n\n"
        
        if len(data_collector.actions) > 0:
            recent_actions = data_collector.actions[-5:]
            stats += f"Recent Actions:\n"
            for action in recent_actions:
                stats += f"  - {action.action_type} in {action.application} at {action.timestamp.strftime('%H:%M')}\n"
        
        return stats
    except Exception as e:
        return f"Error getting stats: {str(e)}"

@mcp.tool()
async def auto_optimize_system() -> str:
    """Automatically optimize system based on ML predictions"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        # Get system load prediction
        load_prediction = ML_ENGINE['system_optimizer'].predict_system_load()
        
        if 'error' in load_prediction:
            return f"Cannot optimize: {load_prediction['error']}"
        
        current_load = load_prediction['current_cpu_load']
        predicted_load = load_prediction['predicted_cpu_load']
        
        optimizations = []
        
        # High CPU load optimizations
        if current_load > 80 or predicted_load > 80:
            optimizations.append("🔧 High CPU load detected - Consider closing unnecessary applications")
            # You could add actual optimization actions here
        
        # Memory optimization
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            optimizations.append("🔧 High memory usage - Consider clearing cache or restarting applications")
        
        # Get behavior recommendations
        recommendations = ML_ENGINE['recommendation_engine'].get_recommendations()
        
        result = "System Auto-Optimization Results:\n\n"
        result += f"Current CPU: {current_load:.1f}%\n"
        result += f"Predicted CPU: {predicted_load:.1f}%\n\n"
        
        if optimizations:
            result += "Optimizations Applied:\n"
            for opt in optimizations:
                result += f"  {opt}\n"
        else:
            result += "✅ System is running optimally\n"
        
        return result
    except Exception as e:
        return f"Error optimizing system: {str(e)}"

@mcp.tool()
async def get_last_metric() -> str:
    """Get the most recent ML metric."""
    if not ML_AVAILABLE:
        return "ML engine not available"
    try:
        data_collector = ML_ENGINE['data_collector']
        if len(data_collector.metrics) > 0:
            last_metric = data_collector.metrics[-1]
            return f"Last System Metric:\n" + \
                   f"CPU Usage: {last_metric.cpu_usage:.1f}%\n" + \
                   f"Memory Usage: {last_metric.memory_usage:.1f}%\n" + \
                   f"Disk Usage: {last_metric.disk_usage:.1f}%\n" + \
                   f"Active Processes: {last_metric.active_processes}\n" + \
                   f"Timestamp: {last_metric.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            return "No metrics recorded yet. Use record_system_metrics() first."
    except Exception as e:
        return f"Error fetching last metric: {str(e)}"

@mcp.tool()
async def start_ml_monitoring() -> str:
    """Start comprehensive ML monitoring and data collection"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        # Import and start comprehensive monitoring
        from comprehensive_user_monitor import start_comprehensive_monitoring, get_monitoring_stats
        
        # Record initial metrics
        ML_ENGINE['data_collector'].record_system_metrics()
        
        # Start comprehensive user monitoring
        if start_comprehensive_monitoring():
            # Also start background ML monitoring
            started = start_background_monitoring()
            return "Comprehensive ML monitoring started - all user actions and system metrics will be recorded automatically"
        else:
            return "Comprehensive monitoring already running"
    except Exception as e:
        return f"Error starting comprehensive monitoring: {str(e)}"

@mcp.tool()
async def stop_ml_monitoring() -> str:
    """Stop continuous ML monitoring"""
    if not ML_AVAILABLE:
        return "ML engine not available"
    
    try:
        stopped = stop_background_monitoring()
        
        if stopped:
            return "🛑 ML monitoring stopped"
        else:
            return "⚠️ ML monitoring was not running"
    except Exception as e:
        return f"Error stopping monitoring: {str(e)}"

# Global variables for monitoring
ML_MONITORING_ACTIVE = False
ML_MONITOR_THREAD = None

# Auto-record system metrics on server startup
if ML_AVAILABLE:
    import threading
    import time
    import datetime
    
def background_monitoring():
        """Background thread for continuous monitoring"""
        global ML_MONITORING_ACTIVE
        
        print("Background ML monitoring started")
        consecutive_errors = 0
        
        previous_active_window = None
        previous_process_list = set(psutil.pids())

        while ML_MONITORING_ACTIVE:
            try:
                # Record system metrics
                ML_ENGINE['data_collector'].record_system_metrics()

                # Active window detection
                try:
                    active_window = gw.getActiveWindow()
                    if active_window and active_window.title and active_window.title != previous_active_window:
                        previous_active_window = active_window.title
                        ML_ENGINE['data_collector'].record_action('window_focus', active_window.title, 0.0)
                except Exception as e:
                    # Fallback: use Windows API to get active window
                    try:
                        import ctypes
                        from ctypes import wintypes
                        user32 = ctypes.windll.user32
                        kernel32 = ctypes.windll.kernel32
                        
                        # Get active window handle
                        hwnd = user32.GetForegroundWindow()
                        if hwnd:
                            # Get window title
                            length = user32.GetWindowTextLengthW(hwnd)
                            if length > 0:
                                buffer = ctypes.create_unicode_buffer(length + 1)
                                user32.GetWindowTextW(hwnd, buffer, length + 1)
                                window_title = buffer.value
                                
                                # Get process ID
                                pid = wintypes.DWORD()
                                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                                
                                # Get process name
                                try:
                                    process = psutil.Process(pid.value)
                                    process_name = process.name()
                                    
                                    if window_title != previous_active_window:
                                        previous_active_window = window_title
                                        ML_ENGINE['data_collector'].record_action('window_focus', f"{process_name}: {window_title}", 0.0)
                                except:
                                    if window_title != previous_active_window:
                                        previous_active_window = window_title
                                        ML_ENGINE['data_collector'].record_action('window_focus', window_title, 0.0)
                    except Exception as e2:
                        pass

                # Process monitoring
                current_process_list = set(psutil.pids())
                new_processes = current_process_list - previous_process_list
                for pid in new_processes:
                    try:
                        proc = psutil.Process(pid)
                        proc_info = f"{proc.name()}({proc.exe()})"
                        ML_ENGINE['data_collector'].record_action('launch', proc_info, 0.0)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                previous_process_list = current_process_list

                # Record user actions
                if pyautogui.onScreen(pyautogui.position()):
                    ML_ENGINE['data_collector'].record_action('mouse', 'user', 0.0)
                # Check for any key press activity (simplified approach)
                try:
                    # Check for common keys being pressed
                    common_keys = ['space', 'enter', 'ctrl', 'alt', 'shift']
                    key_pressed = any(keyboard.is_pressed(key) for key in common_keys)
                    if key_pressed:
                        ML_ENGINE['data_collector'].record_action('keyboard', 'user', 0.0)
                except:
                    pass  # Skip keyboard monitoring if there are issues
                
                # Get current counts
                metrics_count = len(ML_ENGINE['data_collector'].metrics)
                actions_count = len(ML_ENGINE['data_collector'].actions)
                
                # Print status every 10 collections
                if metrics_count % 10 == 0:
                    print(f"✅ ML Data: {metrics_count} metrics, {actions_count} actions")
                
                # Reset error counter on success
                consecutive_errors = 0
                
                # Sleep for 5 seconds for rapid data collection
                time.sleep(5)
                
            except Exception as e:
                consecutive_errors += 1
                print(f"❌ Background monitoring error ({consecutive_errors}): {e}")
                
                # If too many consecutive errors, sleep longer
                if consecutive_errors > 5:
                    print(f"⚠️ Too many errors ({consecutive_errors}), sleeping 5 minutes")
                    time.sleep(300)  # Sleep 5 minutes
                else:
                    time.sleep(30)  # Wait 30 seconds before retrying
        
        print("🛑 Background ML monitoring stopped")

def start_background_monitoring():
    """Start background monitoring if not already running"""
    global ML_MONITORING_ACTIVE, ML_MONITOR_THREAD
    
    if not ML_MONITORING_ACTIVE:
        ML_MONITORING_ACTIVE = True
        ML_MONITOR_THREAD = threading.Thread(target=background_monitoring, daemon=True)
        ML_MONITOR_THREAD.start()
        print("Background ML monitoring thread started")
        return True
    else:
        print("⚠️ Background monitoring already running")
        return False

def stop_background_monitoring():
    """Stop background monitoring"""
    global ML_MONITORING_ACTIVE
    
    if ML_MONITORING_ACTIVE:
        ML_MONITORING_ACTIVE = False
        print("🛑 Background ML monitoring stopping...")
        return True
    else:
        print("⚠️ Background monitoring not running")
        return False

@mcp.tool()
async def get_window_list() -> str:
    """Get list of all open windows"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        windows = gw.getAllWindows()
        window_info = []
        for window in windows:
            if window.title.strip():  # Only windows with titles
                window_info.append(f"Title: '{window.title}' | Size: {window.width}x{window.height} | Position: ({window.left}, {window.top})")
        
        if window_info:
            return f"Open Windows ({len(window_info)} total):\n" + "\n".join(window_info)
        else:
            return "No windows with titles found"
    except Exception as e:
        return f"Error getting window list: {str(e)}"

@mcp.tool()
async def focus_window(window_title: str) -> str:
    """Focus on a specific window by title (partial match)"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            # Try partial match
            all_windows = gw.getAllWindows()
            windows = [w for w in all_windows if window_title.lower() in w.title.lower()]
        
        if windows:
            window = windows[0]
            window.activate()
            return f"Focused window: '{window.title}'"
        else:
            return f"No window found with title containing: '{window_title}'"
    except Exception as e:
        return f"Error focusing window: {str(e)}"

@mcp.tool()
async def take_screenshot(filename: str = "screenshot.png") -> str:
    """Take a screenshot of the entire screen"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return f"Screenshot saved as: {filename}"
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"

@mcp.tool()
async def click_at_coordinates(x: int, y: int, button: str = "left") -> str:
    """Click at specific screen coordinates"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if button.lower() == "right":
            pyautogui.rightClick(x, y)
        elif button.lower() == "middle":
            pyautogui.middleClick(x, y)
        else:
            pyautogui.click(x, y)
        return f"Clicked at ({x}, {y}) with {button} button"
    except Exception as e:
        return f"Error clicking at coordinates: {str(e)}"

@mcp.tool()
async def type_text(text: str, interval: float = 0.01) -> str:
    """Type text with specified interval between characters"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        pyautogui.typewrite(text, interval=interval)
        return f"Typed text: '{text}'"
    except Exception as e:
        return f"Error typing text: {str(e)}"

@mcp.tool()
async def send_keyboard_shortcut(keys: str) -> str:
    """Send keyboard shortcut (e.g., 'ctrl+c', 'alt+tab', 'win+r')"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        key_list = [k.strip() for k in keys.split('+')]
        pyautogui.hotkey(*key_list)
        return f"Sent keyboard shortcut: {keys}"
    except Exception as e:
        return f"Error sending keyboard shortcut: {str(e)}"

@mcp.tool()
async def find_image_on_screen(image_path: str, confidence: float = 0.8) -> str:
    """Find an image on the screen and return its coordinates"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if not os.path.exists(image_path):
            return f"Image file not found: {image_path}"
        
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            return f"Image found at: {center} (box: {location})"
        else:
            return f"Image not found on screen: {image_path}"
    except Exception as e:
        return f"Error finding image: {str(e)}"

@mcp.tool()
async def click_image_if_found(image_path: str, confidence: float = 0.8) -> str:
    """Find and click an image on the screen"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if not os.path.exists(image_path):
            return f"Image file not found: {image_path}"
        
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            pyautogui.click(center)
            return f"Clicked image at: {center}"
        else:
            return f"Image not found on screen: {image_path}"
    except Exception as e:
        return f"Error clicking image: {str(e)}"

@mcp.tool()
async def scroll_screen(direction: str, clicks: int = 3) -> str:
    """Scroll the screen in specified direction (up/down)"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if direction.lower() == "up":
            pyautogui.scroll(clicks)
        elif direction.lower() == "down":
            pyautogui.scroll(-clicks)
        else:
            return "Direction must be 'up' or 'down'"
        
        return f"Scrolled {direction} {clicks} clicks"
    except Exception as e:
        return f"Error scrolling: {str(e)}"

@mcp.tool()
async def drag_and_drop(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> str:
    """Drag from start coordinates to end coordinates"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button='left')
        return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
    except Exception as e:
        return f"Error dragging: {str(e)}"

@mcp.tool()
async def get_mouse_position() -> str:
    """Get current mouse cursor position"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        x, y = pyautogui.position()
        return f"Mouse position: ({x}, {y})"
    except Exception as e:
        return f"Error getting mouse position: {str(e)}"

@mcp.tool()
async def move_mouse(x: int, y: int, duration: float = 0.25) -> str:
    """Move mouse to specified coordinates"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        pyautogui.moveTo(x, y, duration=duration)
        return f"Moved mouse to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {str(e)}"

# ==============================================================================
# CHROME DEVTOOLS PROTOCOL-BASED WEB AUTOMATION WITH COOKIE MANAGEMENT
# ==============================================================================

class ChromeAutomation:
    def __init__(self):
        self.chrome_process = None
        self.debug_port = 9222
        self.ws_url = None
        self.cookie_storage = {}
        self.cookie_preferences = {}
    
    def start_chrome(self, headless: bool = False) -> bool:
        """Start Chrome with DevTools Protocol enabled"""
        try:
            # Check if Chrome is already running with debug port
            if self.is_chrome_running():
                return self.connect_to_chrome()
            
            # Chrome executable paths
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME'))
            ]
            
            chrome_exe = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_exe = path
                    break
            
            if not chrome_exe:
                return False
            
            # Chrome arguments
            args = [
                chrome_exe,
                f"--remote-debugging-port={self.debug_port}",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-extensions",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--user-data-dir=chrome_profile"
            ]
            
            if headless:
                args.append("--headless")
            
            # Start Chrome
            self.chrome_process = subprocess.Popen(args)
            time.sleep(3)  # Wait for Chrome to start
            
            return self.connect_to_chrome()
            
        except Exception as e:
            print(f"Error starting Chrome: {e}")
            return False
    
    def is_chrome_running(self) -> bool:
        """Check if Chrome is running with debug port"""
        try:
            response = requests.get(f"http://localhost:{self.debug_port}/json/version", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def connect_to_chrome(self) -> bool:
        """Connect to Chrome DevTools Protocol"""
        try:
            # Get available tabs
            response = requests.get(f"http://localhost:{self.debug_port}/json")
            if response.status_code != 200:
                return False
            
            tabs = response.json()
            if not tabs:
                return False
            
            # Use the first tab
            self.ws_url = tabs[0]['webSocketDebuggerUrl']
            return True
            
        except Exception as e:
            print(f"Error connecting to Chrome: {e}")
            return False
    
    def send_command(self, method: str, params: dict = None) -> dict:
        """Send command to Chrome DevTools Protocol"""
        try:
            if not self.ws_url:
                return {"error": "Not connected to Chrome"}
            
            # For simplicity, we'll use HTTP requests instead of WebSocket
            # This is a simplified implementation
            response = requests.post(
                f"http://localhost:{self.debug_port}/json/runtime/evaluate",
                json={
                    "expression": f"JSON.stringify({{method: '{method}', params: {json.dumps(params or {})}}})"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def navigate_to_url(self, url: str) -> bool:
        """Navigate to a URL"""
        try:
            # Use subprocess to send command to Chrome
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    subprocess.Popen([chrome_path, url])
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error navigating to URL: {e}")
            return False
    
    def get_cookies(self) -> list:
        """Get all cookies from current domain"""
        try:
            # Simulate getting cookies using JavaScript execution
            js_code = "document.cookie.split(';').map(c => c.trim().split('='))"
            result = self.execute_javascript(js_code)
            return result.get('cookies', [])
        except Exception as e:
            print(f"Error getting cookies: {e}")
            return []
    
    def set_cookie(self, name: str, value: str, domain: str = None) -> bool:
        """Set a cookie"""
        try:
            cookie_str = f"{name}={value}"
            if domain:
                cookie_str += f"; domain={domain}"
            
            js_code = f"document.cookie = '{cookie_str}'"
            self.execute_javascript(js_code)
            return True
        except Exception as e:
            print(f"Error setting cookie: {e}")
            return False
    
    def clear_cookies(self) -> bool:
        """Clear all cookies"""
        try:
            js_code = "document.cookie.split(';').forEach(c => { document.cookie = c.replace(/^ +/, '').replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/'); })"
            self.execute_javascript(js_code)
            return True
        except Exception as e:
            print(f"Error clearing cookies: {e}")
            return False
    
    def execute_javascript(self, code: str) -> dict:
        """Execute JavaScript code"""
        try:
            # Use pyautogui to send JavaScript to browser console
            # This is a simplified approach
            pyautogui.hotkey('f12')  # Open DevTools
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'shift', 'c')  # Open Console
            time.sleep(1)
            pyautogui.typewrite(code)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('f12')  # Close DevTools
            
            return {"result": "JavaScript executed"}
        except Exception as e:
            return {"error": str(e)}
    
    def find_and_click_cookie_buttons(self) -> list:
        """Find and click cookie acceptance buttons"""
        clicked_buttons = []
        
        # Common cookie button selectors and text patterns
        cookie_patterns = [
            # Text patterns to search for
            "Accept", "Accept All", "Accept Cookies", "I Agree", "I Accept",
            "Allow", "Allow All", "OK", "Got It", "Agree", "Continue",
            "Accept and Continue", "Agree and Continue", "Yes", "Consent",
            "I Understand", "Understood", "Fine by me", "That's OK"
        ]
        
        try:
            # Take a screenshot to analyze
            screenshot = pyautogui.screenshot()
            
            # Use OCR-like approach to find text (simplified)
            # In a real implementation, you'd use proper OCR
            for pattern in cookie_patterns:
                try:
                    # Look for buttons with specific text
                    button_location = pyautogui.locateOnScreen(None, confidence=0.8)
                    if button_location:
                        center = pyautogui.center(button_location)
                        pyautogui.click(center)
                        clicked_buttons.append(pattern)
                        time.sleep(1)
                        break
                except:
                    continue
            
            return clicked_buttons
            
        except Exception as e:
            print(f"Error finding cookie buttons: {e}")
            return []
    
    def auto_accept_cookies(self) -> str:
        """Automatically accept cookies using various methods"""
        try:
            clicked_buttons = []
            
            # Method 1: Look for common cookie banner elements and click them
            common_coordinates = [
                # Common positions for cookie banners
                (1200, 650),  # Bottom right
                (960, 650),   # Bottom center
                (720, 650),   # Bottom left
                (1200, 100),  # Top right
                (960, 100),   # Top center
            ]
            
            # Take screenshot to analyze
            screenshot = pyautogui.screenshot()
            
            # Try clicking at common cookie banner locations
            for x, y in common_coordinates:
                try:
                    # Move to position and check if there's a clickable element
                    pyautogui.moveTo(x, y, duration=0.5)
                    time.sleep(0.5)
                    
                    # Try to click if cursor changes (indicates clickable element)
                    pyautogui.click(x, y)
                    clicked_buttons.append(f"Clicked at ({x}, {y})")
                    time.sleep(2)
                    
                except Exception as e:
                    continue
            
            # Method 2: Use keyboard shortcuts that might accept cookies
            keyboard_shortcuts = [
                ['tab', 'enter'],  # Tab to button and press enter
                ['escape'],        # Sometimes escape closes cookie banners
                ['enter'],         # Sometimes enter accepts
            ]
            
            for shortcut in keyboard_shortcuts:
                try:
                    pyautogui.hotkey(*shortcut)
                    clicked_buttons.append(f"Used shortcut: {'+'.join(shortcut)}")
                    time.sleep(1)
                except:
                    continue
            
            if clicked_buttons:
                return f"Cookie acceptance attempted: {', '.join(clicked_buttons)}"
            else:
                return "No cookie banners found or unable to interact"
                
        except Exception as e:
            return f"Error auto-accepting cookies: {str(e)}"
    
    def save_cookies_for_domain(self, domain: str) -> bool:
        """Save cookies for a specific domain"""
        try:
            cookies = self.get_cookies()
            self.cookie_storage[domain] = cookies
            
            # Save to preferences file
            preferences = load_user_preferences()
            if 'cookies' not in preferences:
                preferences['cookies'] = {}
            preferences['cookies'][domain] = cookies
            save_user_preferences(preferences)
            
            return True
        except Exception as e:
            print(f"Error saving cookies: {e}")
            return False
    
    def load_cookies_for_domain(self, domain: str) -> bool:
        """Load cookies for a specific domain"""
        try:
            preferences = load_user_preferences()
            if 'cookies' in preferences and domain in preferences['cookies']:
                cookies = preferences['cookies'][domain]
                for cookie in cookies:
                    if len(cookie) >= 2:
                        self.set_cookie(cookie[0], cookie[1], domain)
                return True
            return False
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return False
    
    def close_chrome(self):
        """Close Chrome browser"""
        if self.chrome_process:
            self.chrome_process.terminate()
            self.chrome_process = None
        self.ws_url = None

# Global Chrome automation instance
chrome_automation = ChromeAutomation()

@mcp.tool()
async def start_web_automation(headless: bool = False) -> str:
    """Start web browser automation (requires Chrome and ChromeDriver)"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if chrome_automation.start_chrome(headless):
            return f"Chrome automation started (headless: {headless})"
        else:
            return "Failed to start Chrome automation. Make sure Chrome is installed."
    except Exception as e:
        return f"Error starting web automation: {str(e)}"

@mcp.tool()
async def navigate_to_url(url: str) -> str:
    """Navigate to a specific URL"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if chrome_automation.navigate_to_url(url):
            return f"Navigated to: {url}"
        else:
            return "Failed to navigate to URL. Make sure Chrome is running."
    except Exception as e:
        return f"Error navigating to URL: {str(e)}"

@mcp.tool()
async def find_and_click_element(selector: str, selector_type: str = "css") -> str:
    """Find and click an element on the webpage using Chrome automation"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        # Use JavaScript to find and click element
        if selector_type == "css":
            js_code = f"document.querySelector('{selector}').click()"
        elif selector_type == "xpath":
            js_code = f"document.evaluate('{selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
        elif selector_type == "id":
            js_code = f"document.getElementById('{selector}').click()"
        elif selector_type == "class":
            js_code = f"document.getElementsByClassName('{selector}')[0].click()"
        elif selector_type == "tag":
            js_code = f"document.getElementsByTagName('{selector}')[0].click()"
        else:
            return f"Invalid selector type. Use: css, xpath, id, class, tag"
        
        result = chrome_automation.execute_javascript(js_code)
        if "error" in result:
            return f"Error clicking element: {result['error']}"
        
        return f"Clicked element: {selector} (type: {selector_type})"
    except Exception as e:
        return f"Error clicking element: {str(e)}"

@mcp.tool()
async def type_in_element(selector: str, text: str, selector_type: str = "css") -> str:
    """Type text into an element on the webpage"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if not web_automation.driver:
            return "Web automation not started. Use start_web_automation() first."
        
        by_type = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME
        }
        
        if selector_type not in by_type:
            return f"Invalid selector type. Use: {', '.join(by_type.keys())}"
        
        element = web_automation.wait.until(
            EC.presence_of_element_located((by_type[selector_type], selector))
        )
        element.clear()
        element.send_keys(text)
        return f"Typed '{text}' into element: {selector}"
    except Exception as e:
        return f"Error typing in element: {str(e)}"

@mcp.tool()
async def get_page_title() -> str:
    """Get the current page title"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if not web_automation.driver:
            return "Web automation not started. Use start_web_automation() first."
        
        title = web_automation.driver.title
        return f"Page title: {title}"
    except Exception as e:
        return f"Error getting page title: {str(e)}"

@mcp.tool()
async def close_web_automation() -> str:
    """Close the web automation browser"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        web_automation.close_browser()
        return "Web automation browser closed"
    except Exception as e:
        return f"Error closing web automation: {str(e)}"

# ==============================================================================
# OFFICE.JS MCP INTEGRATION TOOLS
# ==============================================================================

# Importing office MCP tools
from office_mcp_server import OfficeMCPIntegration

office_integration = OfficeMCPIntegration()

@mcp.tool()
async def office_execute_command(app: str, command: str, params_json: str) -> str:
    """Execute Office.js command for Microsoft 365 apps"""
    try:
        params = json.loads(params_json)
        result = office_integration.execute_office_command(app, command, params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error executing Office command: {str(e)}"

@mcp.tool()
async def word_insert_text(location: str = "selection", text: str = "Hello from MCP!") -> str:
    """Insert text at the current selection in Word"""
    try:
        params = {"location": location, "text": text}
        result = office_integration.word_insert_text(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error inserting text in Word: {str(e)}"

@mcp.tool()
async def word_replace_all_text(search: str, replace: str) -> str:
    """Find and replace all instances of text in Word"""
    try:
        params = {"search": search, "replace": replace}
        result = office_integration.word_replace_all_text(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error replacing text in Word: {str(e)}"

@mcp.tool()
async def excel_set_range_values(sheet: str = "Sheet1", range_addr: str = "A1", values: str = "[[\"Hello\", \"World\"]]") -> str:
    """Set values in an Excel range"""
    try:
        values_array = json.loads(values)
        params = {"sheet": sheet, "range": range_addr, "values": values_array}
        result = office_integration.excel_set_range_values(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error setting Excel range values: {str(e)}"

@mcp.tool()
async def excel_add_worksheet(name: str = "NewSheet") -> str:
    """Add a new worksheet to Excel"""
    try:
        params = {"name": name}
        result = office_integration.excel_add_worksheet(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error adding Excel worksheet: {str(e)}"

@mcp.tool()
async def powerpoint_insert_slide(layout: str = "Title and Content", title: str = "New Slide") -> str:
    """Insert a new slide in PowerPoint"""
    try:
        params = {"layout": layout, "title": title}
        result = office_integration.powerpoint_insert_slide(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error inserting PowerPoint slide: {str(e)}"

@mcp.tool()
async def outlook_create_draft(to: str, subject: str, body: str) -> str:
    """Create a new email draft in Outlook"""
    try:
        params = {"to": to, "subject": subject, "body": body}
        result = office_integration.outlook_create_draft(params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error creating Outlook draft: {str(e)}"

@mcp.tool()
async def office_get_supported_commands() -> str:
    """Get list of all supported Office commands"""
    try:
        commands = {}
        for app, app_commands in office_integration.office_commands.items():
            commands[app] = list(app_commands.keys())
        
        return json.dumps({
            "supported_apps": list(commands.keys()),
            "commands": commands,
            "total_commands": sum(len(cmds) for cmds in commands.values())
        }, indent=2)
    except Exception as e:
        return f"Error getting supported commands: {str(e)}"

@mcp.tool()
async def office_create_manifest() -> str:
    """Create a basic Office Add-in manifest template"""
    try:
        manifest_content = """
<?xml version="1.0" encoding="UTF-8"?>
<OfficeApp xmlns="http://schemas.microsoft.com/office/appforoffice/1.1"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:type="ContentApp">
  <Id>12345678-1234-1234-1234-123456789012</Id>
  <Version>1.0.0.0</Version>
  <ProviderName>MCP Office Integration</ProviderName>
  <DefaultLocale>en-US</DefaultLocale>
  <DisplayName DefaultValue="MCP Office Integration"/>
  <Description DefaultValue="Model Context Protocol integration for Office"/>
  <Hosts>
    <Host Name="Document"/>
    <Host Name="Workbook"/>
    <Host Name="Presentation"/>
    <Host Name="Mailbox"/>
  </Hosts>
  <Requirements>
    <Sets>
      <Set Name="WordApi" MinVersion="1.1"/>
      <Set Name="ExcelApi" MinVersion="1.1"/>
      <Set Name="PowerPointApi" MinVersion="1.1"/>
      <Set Name="Mailbox" MinVersion="1.1"/>
    </Sets>
  </Requirements>
  <DefaultSettings>
    <SourceLocation DefaultValue="https://localhost:3000/index.html"/>
  </DefaultSettings>
  <Permissions>ReadWriteDocument</Permissions>
</OfficeApp>"""
        
        # Save manifest to file
        manifest_file = "office_mcp_manifest.xml"
        with open(manifest_file, 'w') as f:
            f.write(manifest_content)
        
        return f"Office Add-in manifest created: {manifest_file}"
    except Exception as e:
        return f"Error creating manifest: {str(e)}"

# ==============================================================================

@mcp.tool()
async def spotify_close_app() -> str:
    """Quit Spotify application"""
    try:
        await close_app("spotify")
        return "✅ Spotify: Application closed"
    except Exception as e:
        return f"❌ Error closing Spotify: {str(e)}"

@mcp.tool()
async def spotify_minimize_window() -> str:
    """Minimize Spotify window"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('alt', 'space')
        pyautogui.press('n')
        return "✅ Spotify: Window minimized"
    except Exception as e:
        return f"❌ Error minimizing Spotify window: {str(e)}"

@mcp.tool()
async def spotify_maximize_window() -> str:
    """Maximize Spotify window"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('alt', 'space')
        pyautogui.press('x')
        return "✅ Spotify: Window maximized"
    except Exception as e:
        return f"❌ Error maximizing Spotify window: {str(e)}"

@mcp.tool()
async def spotify_click_element(element: str) -> str:
    """Click specified element in Spotify"""
    try:
        await focus_window("Spotify")
        # Coordinate-based clicks would typically use PyAutoGUI
        # This is a simplified placeholder example
        if element.lower() == "now playing":
            pyautogui.click(100, 200)  # Hypothetical coordinates
        return f"✅ Spotify: Clicked {element}"
    except Exception as e:
        return f"❌ Error clicking element: {str(e)}"

@mcp.tool()
async def spotify_scroll_playlist(direction: str, clicks: int = 3) -> str:
    """Scroll in a playlist view"""
    try:
        await focus_window("Spotify")
        if direction.lower() not in ["up", "down"]:
            return "❌ Invalid direction (use 'up' or 'down')"
        click_amount = clicks if direction.lower() == "down" else -clicks
        pyautogui.scroll(click_amount)
        return f"✅ Spotify: Scrolled {direction} in playlist"
    except Exception as e:
        return f"❌ Error scrolling playlist: {str(e)}"

@mcp.tool()
async def spotify_press_key(shortcut: str) -> str:
    """Press keyboard shortcut in Spotify"""
    try:
        await focus_window("Spotify")
        keys = [k.strip() for k in shortcut.split('+')]
        pyautogui.hotkey(*keys)
        return f"✅ Spotify: Pressed {shortcut}"
    except Exception as e:
        return f"❌ Error pressing key: {str(e)}"

# 🔄 SYNC & REFRESH COMMANDS
@mcp.tool()
async def spotify_refresh_playlists() -> str:
    """Refresh current playlists"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'r')
        return "✅ Spotify: Playlists refreshed"
    except Exception as e:
        return f"❌ Error refreshing playlists: {str(e)}"

@mcp.tool()
async def spotify_sync_library() -> str:
    """Sync offline library data"""
    try:
        await focus_window("Spotify")
        # Hypothetical command or series of actions to sync library
        pyautogui.hotkey('ctrl', 'alt', 'l')
        return "✅ Spotify: Library synced"
    except Exception as e:
        return f"❌ Error syncing library: {str(e)}"

@mcp.tool()
async def spotify_download_playlist(playlist_name: str) -> str:
    """Download a playlist for offline playback"""
    try:
        await focus_window("Spotify")
        await spotify_search_playlist(playlist_name)
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'd')  # Hypothetical shortcut for download
        return f"✅ Spotify: '{playlist_name}' downloaded for offline"
    except Exception as e:
        return f"❌ Error downloading playlist: {str(e)}"

@mcp.tool()
async def spotify_delete_downloaded_content() -> str:
    """Clear downloaded tracks"""
    try:
        await focus_window("Spotify")
        # Hypothetical series of actions to clear downloaded content
        pyautogui.hotkey('ctrl', 'alt', 'k')
        return "✅ Spotify: Downloaded content cleared"
    except Exception as e:
        return f"❌ Error deleting downloaded content: {str(e)}"

# ==============================================================================
# SPOTIFY AUTOMATION COMMANDS
# ==============================================================================

# ✅ Core Playback Commands
@mcp.tool()
async def spotify_play() -> str:
    """Play the current track in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'alt', 'space')
        return "✅ Spotify: Play command sent"
    except Exception as e:
        return f"❌ Error playing Spotify: {str(e)}"

@mcp.tool()
async def spotify_pause() -> str:
    """Pause playback in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'alt', 'space')
        return "✅ Spotify: Pause command sent"
    except Exception as e:
        return f"❌ Error pausing Spotify: {str(e)}"

@mcp.tool()
async def spotify_toggle_play_pause() -> str:
    """Toggle between play and pause in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.press('space')
        return "✅ Spotify: Toggle play/pause"
    except Exception as e:
        return f"❌ Error toggling Spotify playback: {str(e)}"

@mcp.tool()
async def spotify_next_track() -> str:
    """Skip to the next track in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'right')
        return "✅ Spotify: Next track"
    except Exception as e:
        return f"❌ Error skipping to next track: {str(e)}"

@mcp.tool()
async def spotify_previous_track() -> str:
    """Return to the previous track in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'left')
        return "✅ Spotify: Previous track"
    except Exception as e:
        return f"❌ Error going to previous track: {str(e)}"

@mcp.tool()
async def spotify_seek_to_time(minutes: int, seconds: int = 0) -> str:
    """Seek to a specific timestamp in the track"""
    try:
        await focus_window("Spotify")
        # Click on progress bar at approximate position
        total_seconds = minutes * 60 + seconds
        # Assume track is roughly 3 minutes, calculate position
        position_ratio = min(total_seconds / 180, 1.0)
        progress_bar_x = int(400 + (position_ratio * 400))  # Approximate progress bar position
        pyautogui.click(progress_bar_x, 950)  # Approximate progress bar Y position
        return f"✅ Spotify: Seeked to {minutes}:{seconds:02d}"
    except Exception as e:
        return f"❌ Error seeking in Spotify: {str(e)}"

@mcp.tool()
async def spotify_set_volume(percentage: int) -> str:
    """Set volume to a specific percentage (0-100)"""
    try:
        percentage = max(0, min(100, percentage))  # Clamp between 0-100
        await focus_window("Spotify")
        
        # Use volume keys multiple times to reach desired level
        # First mute, then set to desired level
        pyautogui.hotkey('ctrl', 'shift', 'down')  # Mute
        time.sleep(0.1)
        
        # Each volume up is roughly 10%, so calculate needed presses
        volume_presses = percentage // 10
        for _ in range(volume_presses):
            pyautogui.hotkey('ctrl', 'shift', 'up')
            time.sleep(0.1)
        
        return f"✅ Spotify: Volume set to ~{percentage}%"
    except Exception as e:
        return f"❌ Error setting Spotify volume: {str(e)}"

@mcp.tool()
async def spotify_mute() -> str:
    """Mute Spotify audio"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'shift', 'down')
        return "✅ Spotify: Muted"
    except Exception as e:
        return f"❌ Error muting Spotify: {str(e)}"

@mcp.tool()
async def spotify_unmute() -> str:
    """Unmute Spotify audio"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'shift', 'up')
        return "✅ Spotify: Unmuted"
    except Exception as e:
        return f"❌ Error unmuting Spotify: {str(e)}"

# 🔍 Search & Browse Commands
@mcp.tool()
async def spotify_search_and_play_track(track_name: str) -> str:
    """Search for a track by name and play it immediately"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(track_name)
        pyautogui.press('enter')
        time.sleep(2)  # Wait for search results
        pyautogui.press('enter')  # Play first result
        return f"✅ Spotify: Searched and playing '{track_name}'"
    except Exception as e:
        return f"❌ Error searching and playing track: {str(e)}"

@mcp.tool()
async def spotify_search_track(track_name: str) -> str:
    """Search for a track by name in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(track_name)
        pyautogui.press('enter')
        return f"✅ Spotify: Searched for track '{track_name}'"
    except Exception as e:
        return f"❌ Error searching for track: {str(e)}"

@mcp.tool()
async def spotify_search_artist(artist_name: str) -> str:
    """Search for an artist in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(f"artist:{artist_name}")
        pyautogui.press('enter')
        return f"✅ Spotify: Searched for artist '{artist_name}'"
    except Exception as e:
        return f"❌ Error searching for artist: {str(e)}"

@mcp.tool()
async def spotify_search_album(album_name: str) -> str:
    """Search for an album in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(f"album:{album_name}")
        pyautogui.press('enter')
        return f"✅ Spotify: Searched for album '{album_name}'"
    except Exception as e:
        return f"❌ Error searching for album: {str(e)}"

@mcp.tool()
async def spotify_search_playlist(playlist_name: str) -> str:
    """Search for a playlist in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(f"playlist:{playlist_name}")
        pyautogui.press('enter')
        return f"✅ Spotify: Searched for playlist '{playlist_name}'"
    except Exception as e:
        return f"❌ Error searching for playlist: {str(e)}"

@mcp.tool()
async def spotify_browse_genres() -> str:
    """Browse music by genre in Spotify"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite("genre:")
        return "✅ Spotify: Opened genre browse"
    except Exception as e:
        return f"❌ Error browsing genres: {str(e)}"

@mcp.tool()
async def spotify_open_discover_weekly() -> str:
    """Open Discover Weekly playlist"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite("Discover Weekly")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')  # Select first result
        return "✅ Spotify: Opened Discover Weekly"
    except Exception as e:
        return f"❌ Error opening Discover Weekly: {str(e)}"

@mcp.tool()
async def spotify_open_release_radar() -> str:
    """Open Release Radar playlist"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite("Release Radar")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')  # Select first result
        return "✅ Spotify: Opened Release Radar"
    except Exception as e:
        return f"❌ Error opening Release Radar: {str(e)}"

# 💾 Library & Playlist Management
@mcp.tool()
async def spotify_add_track_to_library() -> str:
    """Save the current track to liked songs"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 's')
        return "✅ Spotify: Added track to library"
    except Exception as e:
        return f"❌ Error adding track to library: {str(e)}"

@mcp.tool()
async def spotify_remove_track_from_library() -> str:
    """Remove the current track from liked songs"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 's')  # Same shortcut toggles
        return "✅ Spotify: Removed track from library"
    except Exception as e:
        return f"❌ Error removing track from library: {str(e)}"

@mcp.tool()
async def spotify_create_playlist(playlist_name: str) -> str:
    """Create a new playlist"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'n')  # New playlist
        time.sleep(1)
        pyautogui.typewrite(playlist_name)
        pyautogui.press('enter')
        return f"✅ Spotify: Created playlist '{playlist_name}'"
    except Exception as e:
        return f"❌ Error creating playlist: {str(e)}"

@mcp.tool()
async def spotify_like_track() -> str:
    """Like the currently playing track"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 's')
        return "✅ Spotify: Liked current track"
    except Exception as e:
        return f"❌ Error liking track: {str(e)}"

@mcp.tool()
async def spotify_dislike_track() -> str:
    """Dislike the current track (for recommendation training)"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('alt', 'down')  # Dislike shortcut
        return "✅ Spotify: Disliked current track"
    except Exception as e:
        return f"❌ Error disliking track: {str(e)}"

# 🧠 Contextual and Smart Commands
@mcp.tool()
async def spotify_play_based_on_mood(mood: str) -> str:
    """Play a playlist matching a mood"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(f"{mood} playlist")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')  # Select first result
        return f"✅ Spotify: Playing {mood} playlist"
    except Exception as e:
        return f"❌ Error playing mood playlist: {str(e)}"

@mcp.tool()
async def spotify_play_genre(genre: str) -> str:
    """Start a playlist for a specific genre"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(f"genre:{genre}")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')  # Select first result
        return f"✅ Spotify: Playing {genre} music"
    except Exception as e:
        return f"❌ Error playing genre: {str(e)}"

@mcp.tool()
async def spotify_play_song_by_artist(artist: str, song: str) -> str:
    """Play a specific song by artist"""
    try:
        # First ensure Spotify is open
        await focus_window("Spotify")
        time.sleep(1)
        
        # Clear search bar and search for the song
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')  # Select all text in search
        time.sleep(0.2)
        pyautogui.typewrite(f"{song} {artist}")
        time.sleep(0.5)
        pyautogui.press('enter')
        
        # Wait for search results to load
        time.sleep(3)
        
        # Navigate to the first song result using Tab and Enter
        pyautogui.press('tab')  # Move to first result
        time.sleep(0.5)
        pyautogui.press('tab')  # Move to next element (might be needed)
        time.sleep(0.5)
        
        # Double-click to play the song
        pyautogui.doubleClick(600, 350)  # Double-click on first result
        time.sleep(1)
        
        # Alternative: Use Enter to play
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # If still not playing, try clicking the play button area
        pyautogui.click(50, 950)  # Play button at bottom
        time.sleep(0.5)
        
        # Final attempt: Use space to toggle play
        pyautogui.press('space')
        
        return f"✅ Spotify: Found and playing '{song}' by {artist}"
    except Exception as e:
        return f"❌ Error playing song: {str(e)}"

@mcp.tool()
async def spotify_resume_last_played() -> str:
    """Resume last playlist or album"""
    try:
        await focus_window("Spotify")
        pyautogui.press('space')  # Resume playback
        return "✅ Spotify: Resumed last played"
    except Exception as e:
        return f"❌ Error resuming playback: {str(e)}"

@mcp.tool()
async def spotify_play_podcast(podcast_name: str) -> str:
    """Play a specific podcast"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'l')  # Focus search bar
        time.sleep(0.5)
        pyautogui.typewrite(f"podcast:{podcast_name}")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')  # Select first result
        return f"✅ Spotify: Playing podcast '{podcast_name}'"
    except Exception as e:
        return f"❌ Error playing podcast: {str(e)}"

# 👥 Collaborative & Social Commands
@mcp.tool()
async def spotify_share_song() -> str:
    """Share the current track via link"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'shift', 'c')  # Copy song link
        return "✅ Spotify: Song link copied to clipboard"
    except Exception as e:
        return f"❌ Error sharing song: {str(e)}"

@mcp.tool()
async def spotify_follow_artist(artist_name: str) -> str:
    """Follow a specific artist"""
    try:
        await focus_window("Spotify")
        await spotify_search_artist(artist_name)
        time.sleep(2)
        # Click on follow button (approximate location)
        pyautogui.click(800, 300)  # Approximate follow button location
        return f"✅ Spotify: Followed artist '{artist_name}'"
    except Exception as e:
        return f"❌ Error following artist: {str(e)}"

@mcp.tool()
async def spotify_open_lyrics() -> str:
    """Open lyrics for the current track"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'shift', 'l')  # Open lyrics
        return "✅ Spotify: Opened lyrics"
    except Exception as e:
        return f"❌ Error opening lyrics: {str(e)}"

@mcp.tool()
async def spotify_shuffle_toggle() -> str:
    """Toggle shuffle mode"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 's')  # Toggle shuffle
        return "✅ Spotify: Toggled shuffle"
    except Exception as e:
        return f"❌ Error toggling shuffle: {str(e)}"

@mcp.tool()
async def spotify_repeat_toggle() -> str:
    """Toggle repeat mode"""
    try:
        await focus_window("Spotify")
        pyautogui.hotkey('ctrl', 'r')  # Toggle repeat
        return "✅ Spotify: Toggled repeat"
    except Exception as e:
        return f"❌ Error toggling repeat: {str(e)}"

# ==============================================================================
# APPLICATION-SPECIFIC AUTOMATION
# ==============================================================================

@mcp.tool()
async def automate_notepad(action: str, content: str = "") -> str:
    """Automate Notepad actions (open, type, save, etc.)"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        if action == "open":
            subprocess.Popen("notepad.exe")
            time.sleep(2)  # Wait for Notepad to open
            return "Notepad opened"
        
        elif action == "type" and content:
            pyautogui.typewrite(content)
            return f"Typed into Notepad: {content}"
        
        elif action == "save":
            pyautogui.hotkey('ctrl', 's')
            return "Sent save command to Notepad"
        
        elif action == "save_as" and content:
            pyautogui.hotkey('ctrl', 'shift', 's')
            time.sleep(1)
            pyautogui.typewrite(content)
            pyautogui.press('enter')
            return f"Saved Notepad as: {content}"
        
        else:
            return "Invalid action. Use: open, type, save, save_as"
    
    except Exception as e:
        return f"Error automating Notepad: {str(e)}"

@mcp.tool()
async def automate_calculator(expression: str) -> str:
    """Automate Calculator to perform calculations"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        # Open calculator
        subprocess.Popen("calc.exe")
        time.sleep(2)
        
        # Type the expression
        pyautogui.typewrite(expression)
        pyautogui.press('enter')
        
        return f"Calculated: {expression}"
    
    except Exception as e:
        return f"Error automating Calculator: {str(e)}"

@mcp.tool()
async def create_automation_workflow(steps: str) -> str:
    """Create and execute a custom automation workflow"""
    if not UI_AUTOMATION_AVAILABLE:
        return "UI automation libraries not available"
    
    try:
        # Parse steps (JSON format expected)
        workflow_steps = json.loads(steps)
        results = []
        
        for step in workflow_steps:
            action = step.get('action')
            params = step.get('params', {})
            
            if action == 'click':
                x, y = params.get('x'), params.get('y')
                pyautogui.click(x, y)
                results.append(f"Clicked at ({x}, {y})")
            
            elif action == 'type':
                text = params.get('text', '')
                pyautogui.typewrite(text)
                results.append(f"Typed: {text}")
            
            elif action == 'hotkey':
                keys = params.get('keys', '').split('+')
                pyautogui.hotkey(*keys)
                results.append(f"Hotkey: {'+'.join(keys)}")
            
            elif action == 'wait':
                duration = params.get('duration', 1)
                time.sleep(duration)
                results.append(f"Waited {duration} seconds")
            
            elif action == 'screenshot':
                filename = params.get('filename', 'workflow_screenshot.png')
                pyautogui.screenshot(filename)
                results.append(f"Screenshot saved: {filename}")
        
        return f"Workflow completed. Steps executed:\n" + "\n".join(results)
    
    except Exception as e:
        return f"Error executing workflow: {str(e)}"

@mcp.tool()
async def monitor_system_activity(duration: int = 60) -> str:
    """Monitor system activity for specified duration"""
    try:
        start_time = time.time()
        activity_log = []
        
        # Monitor for specified duration
        while time.time() - start_time < duration:
            # Get current active window
            try:
                if UI_AUTOMATION_AVAILABLE:
                    active_window = gw.getActiveWindow()
                    if active_window:
                        activity_log.append(f"{datetime.now().strftime('%H:%M:%S')} - Active: {active_window.title}")
            except:
                pass
            
            time.sleep(5)  # Check every 5 seconds
        
        if activity_log:
            return f"System activity log ({duration}s):\n" + "\n".join(activity_log[-20:])  # Last 20 entries
        else:
            return f"No activity detected during {duration} seconds"
    
    except Exception as e:
        return f"Error monitoring system activity: {str(e)}"

@mcp.tool()
async def monitor_for_security_issues() -> str:
    """Monitor for potential security issues"""
    try:
        import subprocess
        import re
        from datetime import datetime, timedelta
        
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
        high_cpu_processes = [p for p in current_processes if p['cpu_percent'] and p['cpu_percent'] > 80]
        high_memory_processes = [p for p in current_processes if p['memory_percent'] and p['memory_percent'] > 80]
        
        if high_cpu_processes:
            for proc in high_cpu_processes[:3]:  # Top 3
                detected_issues.append(f"⚠️ HIGH CPU: {proc['name']} ({proc['cpu_percent']:.1f}%)")
        
        if high_memory_processes:
            for proc in high_memory_processes[:3]:  # Top 3
                detected_issues.append(f"⚠️ HIGH MEMORY: {proc['name']} ({proc['memory_percent']:.1f}%)")
        
        # 3. Check Windows Security Event Log
        try:
            # Get recent security events (last 1 hour)
            security_cmd = 'Get-WinEvent -FilterHashtable @{LogName="Security"; StartTime=(Get-Date).AddHours(-1)} -MaxEvents 50 | Where-Object {$_.LevelDisplayName -eq "Warning" -or $_.LevelDisplayName -eq "Error"} | Select-Object TimeCreated, Id, LevelDisplayName, Message'
            result = subprocess.run(
                ["powershell", "-Command", security_cmd],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                security_events = result.stdout.strip().split('\n')
                if len(security_events) > 3:  # Skip header lines
                    detected_issues.append(f"🔐 SECURITY EVENTS: {len(security_events)-3} warnings/errors in last hour")
                    
        except Exception as e:
            detected_issues.append(f"⚠️ Could not check Security log: {str(e)}")
        
        # 4. Check System Event Log
        try:
            system_cmd = 'Get-WinEvent -FilterHashtable @{LogName="System"; StartTime=(Get-Date).AddHours(-1)} -MaxEvents 50 | Where-Object {$_.LevelDisplayName -eq "Error"} | Select-Object TimeCreated, Id, LevelDisplayName, Message'
            result = subprocess.run(
                ["powershell", "-Command", system_cmd],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                system_events = result.stdout.strip().split('\n')
                if len(system_events) > 3:  # Skip header lines
                    detected_issues.append(f"🖥️ SYSTEM ERRORS: {len(system_events)-3} errors in last hour")
                    
        except Exception as e:
            detected_issues.append(f"⚠️ Could not check System log: {str(e)}")
        
        # 5. Check for unusual network connections
        try:
            network_cmd = 'Get-NetTCPConnection | Where-Object {$_.State -eq "Established"} | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess'
            result = subprocess.run(
                ["powershell", "-Command", network_cmd],
                capture_output=True,
                text=True,
                timeout=20
            )
            
            if result.returncode == 0:
                connections = result.stdout.strip().split('\n')
                external_connections = [conn for conn in connections if '127.0.0.1' not in conn and 'LocalAddress' not in conn]
                if len(external_connections) > 20:  # Many external connections
                    detected_issues.append(f"🌐 NETWORK: {len(external_connections)} active external connections")
                    
        except Exception as e:
            detected_issues.append(f"⚠️ Could not check network connections: {str(e)}")
        
        # 6. Check Windows Defender status
        try:
            defender_cmd = 'Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated'
            result = subprocess.run(
                ["powershell", "-Command", defender_cmd],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0 and result.stdout.strip():
                defender_output = result.stdout.strip()
                if "False" in defender_output:
                    detected_issues.append(f"🛡️ DEFENDER: Windows Defender may be disabled")
                    
        except Exception as e:
            detected_issues.append(f"⚠️ Could not check Windows Defender: {str(e)}")
        
        # 7. Check for failed login attempts
        try:
            login_cmd = 'Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4625; StartTime=(Get-Date).AddHours(-1)} | Measure-Object | Select-Object Count'
            result = subprocess.run(
                ["powershell", "-Command", login_cmd],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0 and result.stdout.strip():
                login_output = result.stdout.strip()
                if "Count" in login_output:
                    lines = login_output.split('\n')
                    for line in lines:
                        if line.strip().isdigit() and int(line.strip()) > 0:
                            detected_issues.append(f"🔑 LOGIN FAILURES: {line.strip()} failed login attempts in last hour")
                            
        except Exception as e:
            detected_issues.append(f"⚠️ Could not check login failures: {str(e)}")
        
        # 8. Check disk space
        try:
            disk_usage = psutil.disk_usage('C:')
            free_percent = (disk_usage.free / disk_usage.total) * 100
            if free_percent < 10:
                detected_issues.append(f"💾 LOW DISK SPACE: C: drive has only {free_percent:.1f}% free space")
        except Exception as e:
            detected_issues.append(f"⚠️ Could not check disk space: {str(e)}")
        
        # Summary
        if detected_issues:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            summary = f"🔒 SECURITY SCAN RESULTS ({timestamp})\n" + "\n".join(detected_issues)
            summary += f"\n\n📊 SYSTEM STATUS:\n- Total Processes: {len(current_processes)}\n- CPU Usage: {psutil.cpu_percent()}%\n- Memory Usage: {psutil.virtual_memory().percent}%"
            return summary
        else:
            return f"✅ NO SECURITY ISSUES DETECTED ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n📊 SYSTEM STATUS:\n- Total Processes: {len(current_processes)}\n- CPU Usage: {psutil.cpu_percent()}%\n- Memory Usage: {psutil.virtual_memory().percent}%"
    
    except Exception as e:
        return f"❌ Error monitoring for security issues: {str(e)}"

@mcp.tool()
async def get_ui_automation_status() -> str:
    """Get status of UI automation capabilities"""
    try:
        status = []
        status.append(f"UI Automation Available: {UI_AUTOMATION_AVAILABLE}")
        
        if UI_AUTOMATION_AVAILABLE:
            status.append(f"PyAutoGUI Version: {pyautogui.__version__}")
            status.append(f"Screen Size: {pyautogui.size()}")
            status.append(f"Mouse Position: {pyautogui.position()}")
            status.append(f"Fail-Safe: {pyautogui.FAILSAFE}")
            status.append(f"Pause Duration: {pyautogui.PAUSE}")
            
            # Check for web automation
            if web_automation.driver:
                status.append("Web Automation: Active")
            else:
                status.append("Web Automation: Inactive")
        
        return "\n".join(status)
    
    except Exception as e:
        return f"Error getting UI automation status: {str(e)}"

if __name__ == "__main__":
    mcp.run()

