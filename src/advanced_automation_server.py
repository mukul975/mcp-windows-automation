#!/usr/bin/env python3
"""
Advanced Automation Server with Complete UI Control
Full application control for all installed programs
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
from typing import Any, Dict, List, Optional, Tuple
from mcp.server.fastmcp import FastMCP
import ctypes
from ctypes import wintypes
import winreg
import urllib.parse
import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
from PIL import Image, ImageGrab
import threading
import asyncio
import win32gui
import win32con
import win32process
import win32api
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize FastMCP server
mcp = FastMCP("advanced-automation-server")

# User preferences storage
PREFERENCES_FILE = "user_preferences.json"
AUTOMATION_LOG = "automation_log.json"

# Application mappings for common software
APPLICATION_MAPPINGS = {
    # Adobe Creative Suite
    "photoshop": "Adobe Photoshop 2025",
    "illustrator": "Adobe Illustrator 2025", 
    "premiere": "Adobe Premiere Pro 2025",
    "after_effects": "Adobe After Effects 2025",
    "lightroom": "Adobe Lightroom",
    "lightroom_classic": "Adobe Lightroom Classic",
    "media_encoder": "Adobe Media Encoder 2025",
    "acrobat": "Adobe Acrobat",
    
    # Development Tools
    "visual_studio": "Visual Studio Community 2022",
    "android_studio": "Android Studio",
    "unity": "Unity Hub",
    "git": "Git",
    "github": "GitHub CLI",
    
    # 3D & Design
    "blender": "Blender",
    "cinema4d": "Maxon Cinema 4D 2025",
    "davinci": "DaVinci Resolve",
    
    # Games & Entertainment
    "steam": "Steam",
    "counter_strike": "Counter-Strike 2",
    "epic_games": "Epic Games Launcher",
    
    # Utilities
    "7zip": "7-Zip",
    "vlc": "VLC media player",
    "chrome": "Google Chrome",
    "edge": "Microsoft Edge",
    "firefox": "Mozilla Firefox",
    "notepad": "Notepad",
    "calculator": "Calculator",
    "explorer": "File Explorer",
    "powershell": "PowerShell",
    "cmd": "Command Prompt",
    
    # Office & Productivity
    "office": "Microsoft 365",
    "word": "Microsoft Word",
    "excel": "Microsoft Excel",
    "powerpoint": "Microsoft PowerPoint",
    "onenote": "Microsoft OneNote",
    "powerbi": "Microsoft Power BI Desktop",
    
    # System Tools
    "corsair": "Corsair iCUE5 Software",
    "nvidia": "NVIDIA App",
    "nvidia_broadcast": "NVIDIA Broadcast",
    "razer": "Razer Synapse",
    "voicemod": "Voicemod",
    "powertoys": "PowerToys",
    "dropbox": "Dropbox",
    "surfshark": "Surfshark",
    
    # Database & Development
    "mysql": "MySQL Workbench",
    "node": "Node.js",
    "java": "Java",
    "python": "Python"
}

# ==============================================================================
# USER PREFERENCES MANAGEMENT (from previous version)
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

def log_automation_action(action: str, details: dict):
    """Log automation actions for debugging"""
    try:
        log_entry = {
            "timestamp": time.time(),
            "action": action,
            "details": details
        }
        
        logs = []
        if Path(AUTOMATION_LOG).exists():
            with open(AUTOMATION_LOG, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        # Keep only last 100 entries
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(AUTOMATION_LOG, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error logging action: {e}")

# ==============================================================================
# CORE AUTOMATION FUNCTIONS
# ==============================================================================

@mcp.tool()
async def open_app(app_name: str, parameters: str = "") -> str:
    """Launch an application by name with advanced detection and control"""
    try:
        log_automation_action("open_app", {"app_name": app_name, "parameters": parameters})
        
        # Normalize app name
        app_key = app_name.lower().replace(" ", "_").replace("-", "_")
        
        # Check if it's a mapped application
        if app_key in APPLICATION_MAPPINGS:
            target_app = APPLICATION_MAPPINGS[app_key]
        else:
            target_app = app_name
        
        # Method 1: Try direct execution
        try:
            if parameters:
                command = f'"{target_app}" {parameters}'
            else:
                command = target_app
            
            process = subprocess.Popen(command, shell=True)
            time.sleep(2)  # Wait for application to start
            
            # Verify application started
            windows = gw.getWindowsWithTitle(target_app)
            if windows:
                return f"✓ Opened {target_app} (PID: {process.pid})"
        except:
            pass
        
        # Method 2: Search in Start Menu
        try:
            subprocess.run(f'start "" "{target_app}"', shell=True, check=True)
            time.sleep(2)
            return f"✓ Opened {target_app} via Start Menu"
        except:
            pass
        
        # Method 3: Search in Program Files
        program_files = [
            "C:/Program Files",
            "C:/Program Files (x86)",
            "D:/Program Files",
            "D:/Program Files (x86)"
        ]
        
        for base_path in program_files:
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.lower().endswith('.exe') and app_name.lower() in file.lower():
                        try:
                            full_path = os.path.join(root, file)
                            if parameters:
                                command = f'"{full_path}" {parameters}'
                            else:
                                command = f'"{full_path}"'
                            
                            process = subprocess.Popen(command, shell=True)
                            time.sleep(2)
                            return f"✓ Opened {file} from {root} (PID: {process.pid})"
                        except:
                            continue
        
        # Method 4: PowerShell Get-Process approach
        try:
            ps_command = f'Get-Process | Where-Object {{$_.ProcessName -like "*{app_name}*"}} | Select-Object -First 1'
            result = subprocess.run(["powershell", "-Command", ps_command], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip():
                return f"✓ Found running instance of {app_name}"
        except:
            pass
        
        return f"❌ Could not find or launch application: {app_name}"
        
    except Exception as e:
        return f"❌ Error opening app: {str(e)}"

@mcp.tool()
async def close_app(app_name: str) -> str:
    """Close application window with multiple methods"""
    try:
        log_automation_action("close_app", {"app_name": app_name})
        
        closed_windows = []
        
        # Method 1: Close by window title
        windows = gw.getWindowsWithTitle(app_name)
        for window in windows:
            try:
                window.close()
                closed_windows.append(window.title)
            except:
                pass
        
        # Method 2: Close by process name
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if app_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    closed_windows.append(f"Process {proc.info['name']} (PID: {proc.info['pid']})")
            except:
                pass
        
        # Method 3: Use taskkill for stubborn processes
        try:
            result = subprocess.run(f'taskkill /f /im "*{app_name}*"', 
                                  shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                closed_windows.append(f"Forcefully closed {app_name}")
        except:
            pass
        
        if closed_windows:
            return f"✓ Closed: {', '.join(closed_windows)}"
        else:
            return f"❌ No instances of {app_name} found to close"
        
    except Exception as e:
        return f"❌ Error closing app: {str(e)}"

@mcp.tool()
async def click_coordinates(x: int, y: int, button: str = "left", clicks: int = 1) -> str:
    """Simulate mouse click at specified coordinates"""
    try:
        log_automation_action("click_coordinates", {"x": x, "y": y, "button": button, "clicks": clicks})
        
        # Validate coordinates
        screen_width, screen_height = pyautogui.size()
        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            return f"❌ Coordinates ({x}, {y}) are outside screen bounds ({screen_width}x{screen_height})"
        
        # Move to coordinates and click
        pyautogui.moveTo(x, y, duration=0.5)
        
        if button.lower() == "left":
            pyautogui.click(x, y, clicks=clicks)
        elif button.lower() == "right":
            pyautogui.rightClick(x, y)
        elif button.lower() == "middle":
            pyautogui.middleClick(x, y)
        else:
            return f"❌ Invalid button: {button}. Use 'left', 'right', or 'middle'"
        
        return f"✓ Clicked {button} button at ({x}, {y}) {clicks} time(s)"
        
    except Exception as e:
        return f"❌ Error clicking: {str(e)}"

@mcp.tool()
async def type_text(text: str, interval: float = 0.1) -> str:
    """Type text into the currently focused window"""
    try:
        log_automation_action("type_text", {"text": text[:50] + "..." if len(text) > 50 else text})
        
        # Get active window info
        active_window = gw.getActiveWindow()
        window_title = active_window.title if active_window else "Unknown"
        
        # Type the text
        pyautogui.typewrite(text, interval=interval)
        
        return f"✓ Typed text into {window_title} (length: {len(text)} chars)"
        
    except Exception as e:
        return f"❌ Error typing text: {str(e)}"

@mcp.tool()
async def capture_screen(save_path: str = "screenshot.png") -> str:
    """Capture full screen screenshot"""
    try:
        log_automation_action("capture_screen", {"save_path": save_path})
        
        # Capture screenshot
        screenshot = ImageGrab.grab()
        
        # Save to file
        full_path = Path(save_path)
        screenshot.save(full_path)
        
        # Get image info
        width, height = screenshot.size
        file_size = full_path.stat().st_size
        
        return f"✓ Screenshot saved to {full_path} ({width}x{height}, {file_size} bytes)"
        
    except Exception as e:
        return f"❌ Error capturing screen: {str(e)}"

@mcp.tool()
async def run_powershell(script: str) -> str:
    """Execute PowerShell command or script"""
    try:
        log_automation_action("run_powershell", {"script": script[:100] + "..." if len(script) > 100 else script})
        
        # Safety check for dangerous commands
        dangerous_commands = [
            'format', 'Remove-Item -Recurse', 'rm -rf', 'del /s', 'rmdir /s',
            'Stop-Computer', 'Restart-Computer', 'Remove-Computer'
        ]
        
        if any(danger in script for danger in dangerous_commands):
            return f"❌ BLOCKED: Potentially dangerous PowerShell command: {script}"
        
        # Execute PowerShell script
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout.strip()
        if result.stderr:
            output += f"\nErrors: {result.stderr.strip()}"
        
        return f"✓ PowerShell executed:\n{output}"
        
    except subprocess.TimeoutExpired:
        return f"❌ PowerShell script timed out: {script}"
    except Exception as e:
        return f"❌ Error running PowerShell: {str(e)}"

@mcp.tool()
async def navigate_browser(url: str, browser: str = "chrome") -> str:
    """Navigate to specified URL in browser"""
    try:
        log_automation_action("navigate_browser", {"url": url, "browser": browser})
        
        # Browser mappings
        browser_commands = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe"
        }
        
        if browser.lower() not in browser_commands:
            return f"❌ Unsupported browser: {browser}. Use chrome, firefox, or edge"
        
        # Open URL in specified browser
        command = f'"{browser_commands[browser.lower()]}" "{url}"'
        process = subprocess.Popen(command, shell=True)
        
        time.sleep(2)  # Wait for browser to load
        
        return f"✓ Opened {url} in {browser} (PID: {process.pid})"
        
    except Exception as e:
        return f"❌ Error navigating browser: {str(e)}"

@mcp.tool()
async def execute_javascript(js_code: str) -> str:
    """Execute JavaScript in active browser tab using Selenium"""
    try:
        log_automation_action("execute_javascript", {"js_code": js_code[:100] + "..." if len(js_code) > 100 else js_code})
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Connect to existing Chrome session or start new one
        try:
            driver = webdriver.Chrome(options=chrome_options)
            
            # Execute JavaScript
            result = driver.execute_script(f"return {js_code}")
            
            # Close driver
            driver.quit()
            
            return f"✓ JavaScript executed successfully. Result: {result}"
            
        except Exception as e:
            return f"❌ Error executing JavaScript: {str(e)}"
        
    except Exception as e:
        return f"❌ Error setting up JavaScript execution: {str(e)}"

# ==============================================================================
# ADVANCED APPLICATION CONTROL
# ==============================================================================

@mcp.tool()
async def control_adobe_app(app_name: str, action: str, parameters: Dict = {}) -> str:
    """Advanced control for Adobe applications"""
    try:
        adobe_apps = {
            "photoshop": "Adobe Photoshop 2025",
            "illustrator": "Adobe Illustrator 2025",
            "premiere": "Adobe Premiere Pro 2025",
            "after_effects": "Adobe After Effects 2025",
            "lightroom": "Adobe Lightroom",
            "lightroom_classic": "Adobe Lightroom Classic"
        }
        
        if app_name.lower() not in adobe_apps:
            return f"❌ Unsupported Adobe app: {app_name}"
        
        target_app = adobe_apps[app_name.lower()]
        
        if action == "open":
            return await open_app(target_app, parameters.get("file_path", ""))
        elif action == "close":
            return await close_app(target_app)
        elif action == "new_document":
            # Open app first
            await open_app(target_app)
            time.sleep(3)
            # Send Ctrl+N for new document
            pyautogui.hotkey('ctrl', 'n')
            return f"✓ Created new document in {target_app}"
        elif action == "save":
            pyautogui.hotkey('ctrl', 's')
            return f"✓ Saved document in {target_app}"
        elif action == "export":
            pyautogui.hotkey('ctrl', 'shift', 'e')
            return f"✓ Opened export dialog in {target_app}"
        else:
            return f"❌ Unknown action: {action}"
            
    except Exception as e:
        return f"❌ Error controlling Adobe app: {str(e)}"

@mcp.tool()
async def control_development_app(app_name: str, action: str, parameters: Dict = {}) -> str:
    """Advanced control for development applications"""
    try:
        dev_apps = {
            "visual_studio": "Visual Studio Community 2022",
            "android_studio": "Android Studio",
            "unity": "Unity Hub",
            "vscode": "Visual Studio Code"
        }
        
        if app_name.lower() not in dev_apps:
            return f"❌ Unsupported development app: {app_name}"
        
        target_app = dev_apps[app_name.lower()]
        
        if action == "open":
            return await open_app(target_app, parameters.get("project_path", ""))
        elif action == "close":
            return await close_app(target_app)
        elif action == "build":
            pyautogui.hotkey('ctrl', 'shift', 'b')
            return f"✓ Started build in {target_app}"
        elif action == "run":
            pyautogui.hotkey('f5')
            return f"✓ Started debugging in {target_app}"
        elif action == "stop":
            pyautogui.hotkey('shift', 'f5')
            return f"✓ Stopped debugging in {target_app}"
        elif action == "new_file":
            pyautogui.hotkey('ctrl', 'n')
            return f"✓ Created new file in {target_app}"
        else:
            return f"❌ Unknown action: {action}"
            
    except Exception as e:
        return f"❌ Error controlling development app: {str(e)}"

@mcp.tool()
async def control_game_launcher(launcher: str, action: str, game_name: str = "") -> str:
    """Control game launchers and games"""
    try:
        launchers = {
            "steam": "Steam",
            "epic": "Epic Games Launcher",
            "origin": "Origin",
            "uplay": "Ubisoft Connect"
        }
        
        if launcher.lower() not in launchers:
            return f"❌ Unsupported launcher: {launcher}"
        
        target_launcher = launchers[launcher.lower()]
        
        if action == "open":
            return await open_app(target_launcher)
        elif action == "close":
            return await close_app(target_launcher)
        elif action == "launch_game" and game_name:
            # Open launcher first
            await open_app(target_launcher)
            time.sleep(3)
            # Search for game
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(1)
            pyautogui.typewrite(game_name)
            time.sleep(1)
            pyautogui.press('enter')
            return f"✓ Launched {game_name} from {target_launcher}"
        else:
            return f"❌ Unknown action: {action}"
            
    except Exception as e:
        return f"❌ Error controlling game launcher: {str(e)}"

# ==============================================================================
# SYSTEM MONITORING AND CONTROL
# ==============================================================================

@mcp.tool()
async def get_window_list() -> str:
    """Get list of all open windows"""
    try:
        windows = gw.getAllWindows()
        window_list = []
        
        for window in windows:
            if window.title.strip():  # Only include windows with titles
                window_list.append({
                    "title": window.title,
                    "position": f"({window.left}, {window.top})",
                    "size": f"{window.width}x{window.height}",
                    "visible": window.visible,
                    "minimized": window.isMinimized,
                    "maximized": window.isMaximized
                })
        
        if not window_list:
            return "No open windows found"
        
        result = "Open Windows:\n"
        for i, window in enumerate(window_list, 1):
            result += f"{i}. {window['title']} - {window['size']} at {window['position']}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error getting window list: {str(e)}"

@mcp.tool()
async def focus_window(window_title: str) -> str:
    """Focus on a specific window"""
    try:
        windows = gw.getWindowsWithTitle(window_title)
        
        if not windows:
            return f"❌ No window found with title: {window_title}"
        
        window = windows[0]  # Get first match
        window.activate()
        
        return f"✓ Focused on window: {window.title}"
        
    except Exception as e:
        return f"❌ Error focusing window: {str(e)}"

@mcp.tool()
async def automate_workflow(workflow_name: str, steps: List[Dict]) -> str:
    """Execute a series of automation steps"""
    try:
        log_automation_action("automate_workflow", {"workflow_name": workflow_name, "steps": len(steps)})
        
        results = []
        
        for i, step in enumerate(steps, 1):
            action = step.get("action")
            params = step.get("parameters", {})
            
            result = f"Step {i}: "
            
            if action == "open_app":
                result += await open_app(params.get("app_name", ""), params.get("parameters", ""))
            elif action == "click":
                result += await click_coordinates(params.get("x", 0), params.get("y", 0), 
                                                params.get("button", "left"), params.get("clicks", 1))
            elif action == "type":
                result += await type_text(params.get("text", ""), params.get("interval", 0.1))
            elif action == "wait":
                time.sleep(params.get("seconds", 1))
                result += f"✓ Waited {params.get('seconds', 1)} seconds"
            elif action == "hotkey":
                keys = params.get("keys", [])
                pyautogui.hotkey(*keys)
                result += f"✓ Pressed hotkey: {'+'.join(keys)}"
            else:
                result += f"❌ Unknown action: {action}"
            
            results.append(result)
            
            # Small delay between steps
            time.sleep(0.5)
        
        return f"✓ Workflow '{workflow_name}' completed:\n" + "\n".join(results)
        
    except Exception as e:
        return f"❌ Error executing workflow: {str(e)}"

# ==============================================================================
# PREVIOUS FUNCTIONS (Music, System, etc.)
# ==============================================================================

@mcp.tool()
async def set_user_preference(category: str, key: str, value: str) -> str:
    """Set a user preference"""
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

@mcp.tool()
async def get_installed_programs() -> str:
    """Get list of installed programs"""
    try:
        programs = []
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
        
        programs = sorted(list(set(programs)))
        if programs:
            return f"Installed Programs ({len(programs)} total):\n" + "\n".join(programs)
        else:
            return "No installed programs found"
    except Exception as e:
        return f"Error getting installed programs: {str(e)}"

# ==============================================================================
# COOKIE MANAGEMENT FUNCTIONS
# ==============================================================================

# Global web driver instance
driver = None

# Cookie management storage
COOKIE_STORAGE = {}
COOKIE_PREFERENCES = {}

@mcp.tool()
async def start_web_automation(headless: bool = False) -> str:
    """Start web browser automation (requires Chrome and ChromeDriver)"""
    global driver
    try:
        if driver is not None:
            return "✓ Web automation already running"
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        if headless:
            chrome_options.add_argument("--headless")
        
        # Start Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        log_automation_action("start_web_automation", {"headless": headless})
        
        return f"✓ Web automation started (headless: {headless})"
        
    except Exception as e:
        return f"❌ Error starting web automation: {str(e)}"

@mcp.tool()
async def close_web_automation() -> str:
    """Close the web automation browser"""
    global driver
    try:
        if driver is None:
            return "✓ Web automation not running"
        
        driver.quit()
        driver = None
        
        log_automation_action("close_web_automation", {})
        
        return "✓ Web automation closed"
        
    except Exception as e:
        return f"❌ Error closing web automation: {str(e)}"

@mcp.tool()
async def navigate_to_url(url: str) -> str:
    """Navigate to a specific URL"""
    global driver
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        driver.get(url)
        
        log_automation_action("navigate_to_url", {"url": url})
        
        return f"✓ Navigated to {url}"
        
    except Exception as e:
        return f"❌ Error navigating to URL: {str(e)}"

@mcp.tool()
async def accept_cookies_automatically() -> str:
    """Automatically detect and accept cookie banners on current page"""
    global driver
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        # Common cookie acceptance selectors
        cookie_selectors = [
            # Generic button text patterns
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'allow')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ok')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'got it')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'understood')]",
            
            # Common class names and IDs
            "//button[contains(@class, 'accept')]",
            "//button[contains(@class, 'agree')]",
            "//button[contains(@class, 'allow')]",
            "//button[contains(@class, 'consent')]",
            "//button[contains(@class, 'cookie')]",
            "//button[contains(@id, 'accept')]",
            "//button[contains(@id, 'agree')]",
            "//button[contains(@id, 'allow')]",
            "//button[contains(@id, 'consent')]",
            "//button[contains(@id, 'cookie')]",
            
            # Specific popular cookie banner frameworks
            "#onetrust-accept-btn-handler",
            "#cookieChoiceDismiss",
            "button[data-testid*='accept']",
            "button[data-testid*='agree']",
            "button[data-testid*='allow']",
            "[data-cy*='accept']",
            "[data-cy*='agree']",
            "[data-cy*='allow']",
            
            # GDPR specific
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept cookies')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree')]",
            
            # Link elements
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'allow')]",
            
            # Input elements
            "//input[@type='button' and contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
            "//input[@type='submit' and contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
        ]
        
        clicked_elements = []
        
        for selector in cookie_selectors:
            try:
                # Try different selector types
                if selector.startswith('//'):
                    # XPath selector
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    # CSS selector
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            # Scroll to element
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.5)
                            
                            # Click element
                            element.click()
                            clicked_elements.append(element.text or element.get_attribute('value') or selector)
                            
                            # Wait a bit for page to respond
                            time.sleep(1)
                            
                            break
                    except Exception as e:
                        continue
                
                if clicked_elements:
                    break
                    
            except Exception as e:
                continue
        
        log_automation_action("accept_cookies_automatically", {"clicked_elements": clicked_elements})
        
        if clicked_elements:
            return f"✓ Accepted cookies by clicking: {', '.join(clicked_elements)}"
        else:
            return "❌ No cookie acceptance buttons found on current page"
        
    except Exception as e:
        return f"❌ Error accepting cookies: {str(e)}"

@mcp.tool()
async def find_and_click_element(selector: str, selector_type: str = "css") -> str:
    """Find and click an element on the webpage"""
    global driver
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        wait = WebDriverWait(driver, 10)
        
        if selector_type.lower() == "xpath":
            element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
        else:
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        
        # Scroll to element
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        
        # Click element
        element.click()
        
        log_automation_action("find_and_click_element", {"selector": selector, "selector_type": selector_type})
        
        return f"✓ Clicked element: {selector}"
        
    except TimeoutException:
        return f"❌ Element not found or not clickable: {selector}"
    except Exception as e:
        return f"❌ Error clicking element: {str(e)}"

@mcp.tool()
async def type_in_element(selector: str, text: str, selector_type: str = "css") -> str:
    """Type text into an element on the webpage"""
    global driver
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        wait = WebDriverWait(driver, 10)
        
        if selector_type.lower() == "xpath":
            element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
        else:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        
        # Clear existing text and type new text
        element.clear()
        element.send_keys(text)
        
        log_automation_action("type_in_element", {"selector": selector, "text": text[:50], "selector_type": selector_type})
        
        return f"✓ Typed '{text}' into element: {selector}"
        
    except TimeoutException:
        return f"❌ Element not found: {selector}"
    except Exception as e:
        return f"❌ Error typing in element: {str(e)}"

@mcp.tool()
async def get_page_title() -> str:
    """Get the current page title"""
    global driver
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        title = driver.title
        current_url = driver.current_url
        
        log_automation_action("get_page_title", {"title": title, "url": current_url})
        
        return f"✓ Page title: {title}\nURL: {current_url}"
        
    except Exception as e:
        return f"❌ Error getting page title: {str(e)}"

@mcp.tool()
async def save_cookies_for_domain(domain: str) -> str:
    """Save cookies for a specific domain"""
    global driver, COOKIE_STORAGE
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        cookies = driver.get_cookies()
        COOKIE_STORAGE[domain] = cookies
        
        log_automation_action("save_cookies_for_domain", {"domain": domain, "cookie_count": len(cookies)})
        
        return f"✓ Saved {len(cookies)} cookies for domain: {domain}"
        
    except Exception as e:
        return f"❌ Error saving cookies: {str(e)}"

@mcp.tool()
async def load_cookies_for_domain(domain: str) -> str:
    """Load saved cookies for a specific domain"""
    global driver, COOKIE_STORAGE
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        if domain not in COOKIE_STORAGE:
            return f"❌ No saved cookies found for domain: {domain}"
        
        cookies = COOKIE_STORAGE[domain]
        
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                continue
        
        log_automation_action("load_cookies_for_domain", {"domain": domain, "cookie_count": len(cookies)})
        
        return f"✓ Loaded {len(cookies)} cookies for domain: {domain}"
        
    except Exception as e:
        return f"❌ Error loading cookies: {str(e)}"

@mcp.tool()
async def clear_cookies() -> str:
    """Clear all cookies from the current browser session"""
    global driver
    try:
        if driver is None:
            return "❌ Web automation not started. Use start_web_automation() first."
        
        driver.delete_all_cookies()
        
        log_automation_action("clear_cookies", {})
        
        return "✓ Cleared all cookies from browser session"
        
    except Exception as e:
        return f"❌ Error clearing cookies: {str(e)}"

@mcp.tool()
async def set_cookie_preference(domain: str, auto_accept: bool = True) -> str:
    """Set cookie acceptance preference for a domain"""
    global COOKIE_PREFERENCES
    try:
        COOKIE_PREFERENCES[domain] = {
            "auto_accept": auto_accept,
            "timestamp": time.time()
        }
        
        # Save to preferences file
        preferences = load_user_preferences()
        if "cookies" not in preferences:
            preferences["cookies"] = {}
        preferences["cookies"][domain] = COOKIE_PREFERENCES[domain]
        save_user_preferences(preferences)
        
        log_automation_action("set_cookie_preference", {"domain": domain, "auto_accept": auto_accept})
        
        return f"✓ Set cookie preference for {domain}: auto_accept = {auto_accept}"
        
    except Exception as e:
        return f"❌ Error setting cookie preference: {str(e)}"

@mcp.tool()
async def visit_url_with_cookie_handling(url: str, auto_accept_cookies: bool = True) -> str:
    """Visit a URL and automatically handle cookie banners"""
    global driver
    try:
        if driver is None:
            # Start web automation if not already started
            await start_web_automation()
        
        # Navigate to URL
        driver.get(url)
        
        # Wait for page to load
        time.sleep(2)
        
        result = f"✓ Navigated to {url}"
        
        if auto_accept_cookies:
            # Try to accept cookies automatically
            cookie_result = await accept_cookies_automatically()
            result += f"\n{cookie_result}"
        
        log_automation_action("visit_url_with_cookie_handling", {"url": url, "auto_accept_cookies": auto_accept_cookies})
        
        return result
        
    except Exception as e:
        return f"❌ Error visiting URL with cookie handling: {str(e)}"

if __name__ == "__main__":
    mcp.run()
