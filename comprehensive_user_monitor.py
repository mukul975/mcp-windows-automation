#!/usr/bin/env python3
"""
Comprehensive User Activity Monitor
Records everything a user does including:
- Applications opened/closed
- Window switches
- Mouse clicks and movements
- Keyboard input (without storing sensitive content)
- Web browsing activity (URLs visited)
- File system activity
- System events
"""

import os
import sys
import time
import json
import psutil
import ctypes
import threading
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from ctypes import wintypes
import subprocess
import sqlite3
import hashlib

# Windows API imports
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Import pynput for low-level monitoring
try:
    from pynput import mouse, keyboard
    from pynput.mouse import Listener as MouseListener
    from pynput.keyboard import Listener as KeyboardListener
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("Warning: pynput not available. Install with: pip install pynput")

try:
    import pygetwindow as gw
    WINDOW_TRACKING_AVAILABLE = True
except ImportError:
    WINDOW_TRACKING_AVAILABLE = False
    print("Warning: pygetwindow not available. Install with: pip install pygetwindow")

@dataclass
class UserActivity:
    """Comprehensive user activity record"""
    timestamp: datetime
    activity_type: str  # 'window_focus', 'mouse_click', 'key_press', 'app_launch', 'url_visit', 'file_access'
    application: str
    details: str  # Specific details about the activity
    window_title: str = ""
    process_id: int = 0
    duration: float = 0.0
    system_metrics: Dict = None

class ComprehensiveUserMonitor:
    """Monitors all user activities comprehensively"""
    
    def __init__(self, db_path: str = "user_activity.db"):
        self.db_path = db_path
        self.is_monitoring = False
        self.activities: List[UserActivity] = []
        
        # State tracking
        self.current_window = None
        self.current_process_list = set()
        self.mouse_position = (0, 0)
        self.key_press_count = 0
        self.mouse_click_count = 0
        
        # Browser monitoring
        self.browser_processes = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe']
        self.last_url_check = time.time()
        
        # Initialize database
        self._init_database()
        
        # Monitoring threads
        self.threads = []
        
    def _init_database(self):
        """Initialize SQLite database for activity storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    application TEXT NOT NULL,
                    details TEXT,
                    window_title TEXT,
                    process_id INTEGER,
                    duration REAL,
                    system_metrics TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp ON user_activities(timestamp)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_activity_type ON user_activities(activity_type)
            ''')
            
            conn.commit()
            conn.close()
            print(f"Database initialized: {self.db_path}")
        except Exception as e:
            print(f"ERROR: Database initialization failed: {e}")

    def _record_activity(self, activity: UserActivity):
        """Record activity to database and memory with proper error handling"""
        try:
            # Validate required fields
            if not activity.application or not activity.activity_type:
                activity.application = activity.application or "Unknown"
                activity.activity_type = activity.activity_type or "unknown"
            
            # Add to memory
            self.activities.append(activity)
            
            # Keep only last 10000 activities in memory
            if len(self.activities) > 10000:
                self.activities = self.activities[-5000:]
            
            # Save to database with proper locking and retry mechanism
            max_retries = 3
            retry_delay = 0.1
            
            for attempt in range(max_retries):
                try:
                    # Use WAL mode for better concurrent access
                    conn = sqlite3.connect(self.db_path, timeout=10.0)
                    conn.execute('PRAGMA journal_mode=WAL')
                    conn.execute('PRAGMA synchronous=NORMAL')
                    conn.execute('PRAGMA temp_store=memory')
                    conn.execute('PRAGMA mmap_size=268435456')  # 256MB
                    
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO user_activities 
                        (timestamp, activity_type, application, details, window_title, process_id, duration, system_metrics)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        activity.timestamp.isoformat(),
                        activity.activity_type or "unknown",
                        activity.application or "Unknown",
                        activity.details or "",
                        activity.window_title or "",
                        activity.process_id or 0,
                        activity.duration or 0.0,
                        json.dumps(activity.system_metrics) if activity.system_metrics else None
                    ))
                    
                    conn.commit()
                    conn.close()
                    break  # Success, exit retry loop
                    
                except sqlite3.OperationalError as db_error:
                    if conn:
                        conn.close()
                    
                    if "database is locked" in str(db_error) and attempt < max_retries - 1:
                        time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    else:
                        raise db_error
                        
        except Exception as e:
            # Only print error once per minute to avoid spam
            current_time = time.time()
            if not hasattr(self, '_last_error_time') or current_time - self._last_error_time > 60:
                print(f"ERROR: Error recording activity: {e}")
                self._last_error_time = current_time

    def _get_current_system_metrics(self) -> Dict:
        """Get current system metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('C:').percent,
                'active_processes': len(psutil.pids()),
                'network_sent': psutil.net_io_counters().bytes_sent,
                'network_recv': psutil.net_io_counters().bytes_recv,
            }
        except:
            return {}

    def _get_active_window_info(self) -> Optional[Dict]:
        """Get information about the currently active window"""
        try:
            # Method 1: Try pygetwindow
            if WINDOW_TRACKING_AVAILABLE:
                try:
                    active_window = gw.getActiveWindow()
                    if active_window and active_window.title:
                        return {
                            'title': active_window.title,
                            'pid': None,
                            'process_name': None
                        }
                except:
                    pass
            
            # Method 2: Use Windows API
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
                        
                        return {
                            'title': window_title,
                            'pid': pid.value,
                            'process_name': process_name
                        }
                    except:
                        return {
                            'title': window_title,
                            'pid': pid.value,
                            'process_name': 'Unknown'
                        }
        except:
            pass
        
        return None

    def _monitor_window_changes(self):
        """Monitor for window focus changes"""
        print("Starting window monitoring...")
        
        while self.is_monitoring:
            try:
                window_info = self._get_active_window_info()
                
                if window_info and window_info != self.current_window:
                    self.current_window = window_info
                    
                    activity = UserActivity(
                        timestamp=datetime.now(),
                        activity_type='window_focus',
                        application=window_info.get('process_name', 'Unknown'),
                        details=f"Focused window: {window_info.get('title', 'Unknown')}",
                        window_title=window_info.get('title', ''),
                        process_id=window_info.get('pid', 0),
                        system_metrics=self._get_current_system_metrics()
                    )
                    
                    self._record_activity(activity)
                    
                time.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"ERROR: Window monitoring error: {e}")
                time.sleep(5)

    def _monitor_process_changes(self):
        """Monitor for new/closed processes"""
        print("Starting process monitoring...")
        
        # Get initial process list
        self.current_process_list = set(psutil.pids())
        
        while self.is_monitoring:
            try:
                current_processes = set(psutil.pids())
                
                # New processes
                new_processes = current_processes - self.current_process_list
                for pid in new_processes:
                    try:
                        proc = psutil.Process(pid)
                        
                        activity = UserActivity(
                            timestamp=datetime.now(),
                            activity_type='app_launch',
                            application=proc.name(),
                            details=f"Launched: {proc.name()} (PID: {pid})",
                            process_id=pid,
                            system_metrics=self._get_current_system_metrics()
                        )
                        
                        self._record_activity(activity)
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                # Closed processes
                closed_processes = self.current_process_list - current_processes
                for pid in closed_processes:
                    activity = UserActivity(
                        timestamp=datetime.now(),
                        activity_type='app_close',
                        application='Unknown',
                        details=f"Closed process (PID: {pid})",
                        process_id=pid,
                        system_metrics=self._get_current_system_metrics()
                    )
                    
                    self._record_activity(activity)
                
                self.current_process_list = current_processes
                time.sleep(3)  # Check every 3 seconds
                
            except Exception as e:
                print(f"ERROR: Process monitoring error: {e}")
                time.sleep(10)

    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        if pressed:  # Only record press, not release
            self.mouse_click_count += 1
            
            window_info = self._get_active_window_info()
            
            activity = UserActivity(
                timestamp=datetime.now(),
                activity_type='mouse_click',
                application=window_info.get('process_name', 'Unknown') if window_info else 'Unknown',
                details=f"Mouse {button.name} click at ({x}, {y})",
                window_title=window_info.get('title', '') if window_info else '',
                process_id=window_info.get('pid', 0) if window_info else 0,
                system_metrics=self._get_current_system_metrics()
            )
            
            self._record_activity(activity)

    def _on_key_press(self, key):
        """Handle keyboard events"""
        self.key_press_count += 1
        
        # Don't record specific keys for privacy, just count and type
        key_type = "special"
        if hasattr(key, 'char') and key.char:
            key_type = "character"
        
        window_info = self._get_active_window_info()
        
        activity = UserActivity(
            timestamp=datetime.now(),
            activity_type='key_press',
            application=window_info.get('process_name', 'Unknown') if window_info else 'Unknown',
            details=f"Key press: {key_type}",
            window_title=window_info.get('title', '') if window_info else '',
            process_id=window_info.get('pid', 0) if window_info else 0,
            system_metrics=self._get_current_system_metrics()
        )
        
        # Only record every 10th keystroke to avoid spam
        if self.key_press_count % 10 == 0:
            self._record_activity(activity)

    def _monitor_browser_activity(self):
        """Monitor browser URLs and web activity"""
        print("Starting browser monitoring...")
        
        while self.is_monitoring:
            try:
                # Check browser processes
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        proc_name = proc.info.get('name')
                        if proc_name and proc_name.lower() in self.browser_processes:
                            # Record browser activity
                            window_info = self._get_active_window_info()
                            
                            if (window_info and 
                                window_info.get('process_name', '') and
                                window_info.get('process_name', '').lower() in self.browser_processes and
                                window_info.get('title')):
                                
                                # Extract URL from window title (simplified)
                                title = window_info.get('title', '')
                                if any(indicator in title.lower() for indicator in ['http', 'www', '.com', '.org', '.net']):
                                    activity = UserActivity(
                                        timestamp=datetime.now(),
                                        activity_type='url_visit',
                                        application=window_info.get('process_name', 'Browser'),
                                        details=f"Browsing: {title}",
                                        window_title=title,
                                        process_id=window_info.get('pid', 0),
                                        system_metrics=self._get_current_system_metrics()
                                    )
                                    
                                    self._record_activity(activity)
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"ERROR: Browser monitoring error: {e}")
                time.sleep(10)

    def _monitor_file_activity(self):
        """Monitor file system activity"""
        print("Starting file monitoring...")
        
        # This is a simplified version - in production, you'd use Windows API file monitoring
        while self.is_monitoring:
            try:
                # Monitor recent files (simplified approach)
                # In a full implementation, you'd use Windows File System Watcher APIs
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"ERROR: File monitoring error: {e}")
                time.sleep(30)

    def start_monitoring(self):
        """Start comprehensive monitoring"""
        if self.is_monitoring:
            print("WARNING: Monitoring already active")
            return False
        
        print("Starting comprehensive user activity monitoring...")
        self.is_monitoring = True
        
        # Start window monitoring thread
        window_thread = threading.Thread(target=self._monitor_window_changes, daemon=True)
        window_thread.start()
        self.threads.append(window_thread)
        
        # Start process monitoring thread
        process_thread = threading.Thread(target=self._monitor_process_changes, daemon=True)
        process_thread.start()
        self.threads.append(process_thread)
        
        # Start browser monitoring thread
        browser_thread = threading.Thread(target=self._monitor_browser_activity, daemon=True)
        browser_thread.start()
        self.threads.append(browser_thread)
        
        # Start file monitoring thread
        file_thread = threading.Thread(target=self._monitor_file_activity, daemon=True)
        file_thread.start()
        self.threads.append(file_thread)
        
        # Start mouse and keyboard listeners if available
        if PYNPUT_AVAILABLE:
            try:
                self.mouse_listener = MouseListener(on_click=self._on_mouse_click)
                self.mouse_listener.start()
                
                self.keyboard_listener = KeyboardListener(on_press=self._on_key_press)
                self.keyboard_listener.start()
                
                print("Mouse and keyboard monitoring active")
            except Exception as e:
                print(f"WARNING: Could not start input monitoring: {e}")
        
        print("Comprehensive monitoring started!")
        return True

    def stop_monitoring(self):
        """Stop all monitoring"""
        if not self.is_monitoring:
            print("WARNING: Monitoring not active")
            return False
        
        print("STOP: Stopping comprehensive monitoring...")
        self.is_monitoring = False
        
        # Stop input listeners
        if PYNPUT_AVAILABLE:
            try:
                if hasattr(self, 'mouse_listener'):
                    self.mouse_listener.stop()
                if hasattr(self, 'keyboard_listener'):
                    self.keyboard_listener.stop()
            except:
                pass
        
        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        print("Monitoring stopped!")
        return True

    def get_activity_summary(self, hours: int = 24) -> Dict:
        """Get activity summary for the last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            since_time = datetime.now().timestamp() - (hours * 3600)
            since_iso = datetime.fromtimestamp(since_time).isoformat()
            
            # Get activity counts by type
            cursor.execute('''
                SELECT activity_type, COUNT(*) as count
                FROM user_activities 
                WHERE timestamp > ? 
                GROUP BY activity_type
                ORDER BY count DESC
            ''', (since_iso,))
            
            activity_counts = dict(cursor.fetchall())
            
            # Get most used applications
            cursor.execute('''
                SELECT application, COUNT(*) as count
                FROM user_activities 
                WHERE timestamp > ? AND activity_type != 'key_press'
                GROUP BY application
                ORDER BY count DESC
                LIMIT 10
            ''', (since_iso,))
            
            top_apps = dict(cursor.fetchall())
            
            # Get recent activities
            cursor.execute('''
                SELECT timestamp, activity_type, application, details
                FROM user_activities 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (since_iso,))
            
            recent_activities = cursor.fetchall()
            
            conn.close()
            
            return {
                'activity_counts': activity_counts,
                'top_applications': top_apps,
                'recent_activities': recent_activities,
                'total_activities': sum(activity_counts.values()),
                'period_hours': hours
            }
            
        except Exception as e:
            return {'error': str(e)}

    def get_stats(self) -> Dict:
        """Get current monitoring statistics"""
        return {
            'is_monitoring': self.is_monitoring,
            'activities_in_memory': len(self.activities),
            'mouse_clicks': self.mouse_click_count,
            'key_presses': self.key_press_count,
            'database_path': self.db_path,
            'pynput_available': PYNPUT_AVAILABLE,
            'window_tracking_available': WINDOW_TRACKING_AVAILABLE,
            'active_threads': len([t for t in self.threads if t.is_alive()]),
        }

# Global monitor instance
user_monitor = ComprehensiveUserMonitor()

def start_comprehensive_monitoring():
    """Start comprehensive user monitoring"""
    return user_monitor.start_monitoring()

def stop_comprehensive_monitoring():
    """Stop comprehensive user monitoring"""
    return user_monitor.stop_monitoring()

def get_monitoring_stats():
    """Get monitoring statistics"""
    return user_monitor.get_stats()

def get_activity_summary(hours: int = 24):
    """Get activity summary"""
    return user_monitor.get_activity_summary(hours)

if __name__ == "__main__":
    # Test the monitor
    print("Testing Comprehensive User Monitor")
    
    if start_comprehensive_monitoring():
        print("Monitoring started - will run for 30 seconds for testing")
        time.sleep(30)
        
        stats = get_monitoring_stats()
        print(f"Stats: {stats}")
        
        summary = get_activity_summary(1)  # Last 1 hour
        print(f"Summary: {summary}")
        
        stop_comprehensive_monitoring()
    else:
        print("ERROR: Failed to start monitoring")
