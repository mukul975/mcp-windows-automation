#!/usr/bin/env python3
"""
GUI Application for Unified Windows MCP Server
Provides a user-friendly interface for all MCP server features
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import asyncio
import threading
import json
from pathlib import Path
import sys
import os

# Import MCP server functions
try:
    from unified_server import (
        set_user_preference, get_user_preference, list_user_preferences,
        open_youtube_with_search, play_favorite_song, open_app_with_url,
        smart_music_action, add_to_playlist, show_playlist,
        get_system_info, list_processes, get_installed_programs,
        get_startup_programs, run_command
    )
except ImportError as e:
    print(f"Error importing MCP server functions: {e}")
    print("Make sure unified_server.py is in the same directory")
    sys.exit(1)

class MCPServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MCP Server Control Panel")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Configure styles
        self.setup_styles()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_music_tab()
        self.create_system_tab()
        self.create_apps_tab()
        self.create_preferences_tab()
        self.create_command_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#404040', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#404040', foreground='white')
        style.configure('TEntry', fieldbackground='#404040', foreground='white')
        
    def create_music_tab(self):
        """Create the music control tab"""
        music_frame = ttk.Frame(self.notebook)
        self.notebook.add(music_frame, text="🎵 Music")
        
        # Favorite song section
        fav_frame = ttk.LabelFrame(music_frame, text="Favorite Song", padding="10")
        fav_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(fav_frame, text="Set Favorite Song:").pack(anchor='w')
        self.fav_song_var = tk.StringVar()
        fav_entry = ttk.Entry(fav_frame, textvariable=self.fav_song_var, width=50)
        fav_entry.pack(side='left', padx=(0, 10))
        
        ttk.Button(fav_frame, text="Set Favorite", 
                  command=self.set_favorite_song).pack(side='left', padx=5)
        ttk.Button(fav_frame, text="Play Favorite", 
                  command=self.play_favorite).pack(side='left', padx=5)
        
        # Playlist section
        playlist_frame = ttk.LabelFrame(music_frame, text="Playlist", padding="10")
        playlist_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Add to playlist
        add_frame = ttk.Frame(playlist_frame)
        add_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(add_frame, text="Add Song:").pack(anchor='w')
        self.add_song_var = tk.StringVar()
        add_entry = ttk.Entry(add_frame, textvariable=self.add_song_var, width=50)
        add_entry.pack(side='left', padx=(0, 10))
        
        ttk.Button(add_frame, text="Add to Playlist", 
                  command=self.add_to_playlist_gui).pack(side='left', padx=5)
        ttk.Button(add_frame, text="Show Playlist", 
                  command=self.show_playlist).pack(side='left', padx=5)
        
        # YouTube search
        youtube_frame = ttk.Frame(playlist_frame)
        youtube_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(youtube_frame, text="YouTube Search:").pack(anchor='w')
        self.youtube_var = tk.StringVar()
        youtube_entry = ttk.Entry(youtube_frame, textvariable=self.youtube_var, width=50)
        youtube_entry.pack(side='left', padx=(0, 10))
        
        ttk.Button(youtube_frame, text="Search YouTube", 
                  command=self.search_youtube).pack(side='left', padx=5)
        
        # Output area
        self.music_output = scrolledtext.ScrolledText(playlist_frame, height=15, 
                                                     bg='#1e1e1e', fg='white', 
                                                     insertbackground='white')
        self.music_output.pack(fill='both', expand=True, pady=(10, 0))
        
    def create_system_tab(self):
        """Create the system information tab"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="🖥️ System")
        
        # Control buttons
        control_frame = ttk.Frame(system_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="System Info", 
                  command=self.get_system_info).pack(side='left', padx=5)
        ttk.Button(control_frame, text="List Processes", 
                  command=self.list_processes).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Startup Programs", 
                  command=self.get_startup_programs).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Clear", 
                  command=lambda: self.system_output.delete(1.0, tk.END)).pack(side='left', padx=5)
        
        # Output area
        self.system_output = scrolledtext.ScrolledText(system_frame, height=35, 
                                                      bg='#1e1e1e', fg='white', 
                                                      insertbackground='white')
        self.system_output.pack(fill='both', expand=True, padx=10, pady=5)
        
    def create_apps_tab(self):
        """Create the applications tab"""
        apps_frame = ttk.Frame(self.notebook)
        self.notebook.add(apps_frame, text="📱 Applications")
        
        # Control buttons
        control_frame = ttk.Frame(apps_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Installed Programs", 
                  command=self.get_installed_programs).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Open App", 
                  command=self.show_open_app_dialog).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Clear", 
                  command=lambda: self.apps_output.delete(1.0, tk.END)).pack(side='left', padx=5)
        
        # Quick app buttons
        quick_frame = ttk.LabelFrame(apps_frame, text="Quick Launch", padding="10")
        quick_frame.pack(fill='x', padx=10, pady=5)
        
        apps = [
            ("Chrome", "chrome"),
            ("Firefox", "firefox"),
            ("Edge", "edge"),
            ("Notepad", "notepad"),
            ("Calculator", "calculator"),
            ("Explorer", "explorer"),
            ("Command Prompt", "cmd"),
            ("PowerShell", "powershell")
        ]
        
        for i, (name, app) in enumerate(apps):
            ttk.Button(quick_frame, text=name, 
                      command=lambda a=app: self.quick_open_app(a)).grid(row=i//4, column=i%4, padx=5, pady=2)
        
        # Output area
        self.apps_output = scrolledtext.ScrolledText(apps_frame, height=30, 
                                                    bg='#1e1e1e', fg='white', 
                                                    insertbackground='white')
        self.apps_output.pack(fill='both', expand=True, padx=10, pady=5)
        
    def create_preferences_tab(self):
        """Create the preferences tab"""
        pref_frame = ttk.Frame(self.notebook)
        self.notebook.add(pref_frame, text="⚙️ Preferences")
        
        # Set preference section
        set_frame = ttk.LabelFrame(pref_frame, text="Set Preference", padding="10")
        set_frame.pack(fill='x', padx=10, pady=5)
        
        # Category
        ttk.Label(set_frame, text="Category:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.pref_category_var = tk.StringVar()
        ttk.Entry(set_frame, textvariable=self.pref_category_var, width=20).grid(row=0, column=1, padx=(0, 10))
        
        # Key
        ttk.Label(set_frame, text="Key:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.pref_key_var = tk.StringVar()
        ttk.Entry(set_frame, textvariable=self.pref_key_var, width=20).grid(row=0, column=3, padx=(0, 10))
        
        # Value
        ttk.Label(set_frame, text="Value:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.pref_value_var = tk.StringVar()
        ttk.Entry(set_frame, textvariable=self.pref_value_var, width=50).grid(row=1, column=1, columnspan=2, padx=(0, 10), pady=(10, 0))
        
        ttk.Button(set_frame, text="Set Preference", 
                  command=self.set_preference).grid(row=1, column=3, pady=(10, 0))
        
        # Get preference section
        get_frame = ttk.LabelFrame(pref_frame, text="Get Preference", padding="10")
        get_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(get_frame, text="Category:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.get_category_var = tk.StringVar()
        ttk.Entry(get_frame, textvariable=self.get_category_var, width=20).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(get_frame, text="Key:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.get_key_var = tk.StringVar()
        ttk.Entry(get_frame, textvariable=self.get_key_var, width=20).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(get_frame, text="Get Preference", 
                  command=self.get_preference).grid(row=0, column=4, padx=(10, 0))
        ttk.Button(get_frame, text="List All Preferences", 
                  command=self.list_preferences).grid(row=0, column=5, padx=(10, 0))
        
        # Output area
        self.pref_output = scrolledtext.ScrolledText(pref_frame, height=25, 
                                                    bg='#1e1e1e', fg='white', 
                                                    insertbackground='white')
        self.pref_output.pack(fill='both', expand=True, padx=10, pady=5)
        
    def create_command_tab(self):
        """Create the command execution tab"""
        cmd_frame = ttk.Frame(self.notebook)
        self.notebook.add(cmd_frame, text="💻 Command")
        
        # Command input
        input_frame = ttk.LabelFrame(cmd_frame, text="Execute Command", padding="10")
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Command:").pack(anchor='w')
        self.command_var = tk.StringVar()
        cmd_entry = ttk.Entry(input_frame, textvariable=self.command_var, width=80)
        cmd_entry.pack(side='left', padx=(0, 10))
        cmd_entry.bind('<Return>', lambda e: self.execute_command())
        
        ttk.Button(input_frame, text="Execute", 
                  command=self.execute_command).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Clear Output", 
                  command=lambda: self.cmd_output.delete(1.0, tk.END)).pack(side='left', padx=5)
        
        # Quick commands
        quick_cmd_frame = ttk.LabelFrame(cmd_frame, text="Quick Commands", padding="10")
        quick_cmd_frame.pack(fill='x', padx=10, pady=5)
        
        commands = [
            ("Directory Listing", "dir"),
            ("System Info", "systeminfo"),
            ("Network Config", "ipconfig /all"),
            ("Running Tasks", "tasklist"),
            ("Disk Usage", "wmic logicaldisk get size,freespace,caption"),
            ("Environment Variables", "set")
        ]
        
        for i, (name, cmd) in enumerate(commands):
            ttk.Button(quick_cmd_frame, text=name, 
                      command=lambda c=cmd: self.quick_command(c)).grid(row=i//3, column=i%3, padx=5, pady=2, sticky='ew')
        
        # Configure grid weights
        for i in range(3):
            quick_cmd_frame.grid_columnconfigure(i, weight=1)
        
        # Output area
        self.cmd_output = scrolledtext.ScrolledText(cmd_frame, height=25, 
                                                   bg='#1e1e1e', fg='white', 
                                                   insertbackground='white')
        self.cmd_output.pack(fill='both', expand=True, padx=10, pady=5)
        
    def run_async(self, func, *args, **kwargs):
        """Run async function in a separate thread"""
        def run_in_thread():
            try:
                self.status_var.set("Processing...")
                self.root.update()
                
                # Run the async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(func(*args, **kwargs))
                loop.close()
                
                self.status_var.set("Completed")
                return result
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                return None
        
        return run_in_thread()
    
    # Music tab methods
    def set_favorite_song(self):
        song = self.fav_song_var.get().strip()
        if not song:
            messagebox.showwarning("Warning", "Please enter a song name")
            return
        
        def execute():
            result = self.run_async(set_user_preference, 'music', 'favorite_song', song)
            if result:
                self.music_output.insert(tk.END, f"✓ {result}\n")
                self.music_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def play_favorite(self):
        def execute():
            result = self.run_async(play_favorite_song)
            if result:
                self.music_output.insert(tk.END, f"🎵 {result}\n")
                self.music_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def add_to_playlist_gui(self):
        song = self.add_song_var.get().strip()
        if not song:
            messagebox.showwarning("Warning", "Please enter a song name")
            return
        
        def execute():
            result = self.run_async(add_to_playlist, song)
            if result:
                self.music_output.insert(tk.END, f"📝 {result}\n")
                self.music_output.see(tk.END)
                self.add_song_var.set("")
        
        threading.Thread(target=execute).start()
    
    def show_playlist(self):
        def execute():
            result = self.run_async(show_playlist)
            if result:
                self.music_output.insert(tk.END, f"📋 {result}\n\n")
                self.music_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def search_youtube(self):
        query = self.youtube_var.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        def execute():
            result = self.run_async(open_youtube_with_search, query)
            if result:
                self.music_output.insert(tk.END, f"🔍 {result}\n")
                self.music_output.see(tk.END)
                self.youtube_var.set("")
        
        threading.Thread(target=execute).start()
    
    # System tab methods
    def get_system_info(self):
        def execute():
            result = self.run_async(get_system_info)
            if result:
                self.system_output.insert(tk.END, f"🖥️ System Information:\n{result}\n\n")
                self.system_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def list_processes(self):
        def execute():
            result = self.run_async(list_processes)
            if result:
                self.system_output.insert(tk.END, f"🔄 Running Processes:\n{result}\n\n")
                self.system_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def get_startup_programs(self):
        def execute():
            result = self.run_async(get_startup_programs)
            if result:
                self.system_output.insert(tk.END, f"🚀 Startup Programs:\n{result}\n\n")
                self.system_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    # Apps tab methods
    def get_installed_programs(self):
        def execute():
            result = self.run_async(get_installed_programs)
            if result:
                self.apps_output.insert(tk.END, f"📱 Installed Programs:\n{result}\n\n")
                self.apps_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def quick_open_app(self, app_name):
        def execute():
            result = self.run_async(open_app_with_url, app_name)
            if result:
                self.apps_output.insert(tk.END, f"🚀 {result}\n")
                self.apps_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def show_open_app_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Open Application")
        dialog.geometry("400x150")
        dialog.configure(bg='#2b2b2b')
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # App name
        ttk.Label(dialog, text="Application Name:").pack(pady=10)
        app_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=app_var, width=40).pack(pady=5)
        
        # URL (optional)
        ttk.Label(dialog, text="URL/Parameters (optional):").pack(pady=(10, 0))
        url_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=url_var, width=40).pack(pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        def open_app():
            app_name = app_var.get().strip()
            url = url_var.get().strip()
            
            if not app_name:
                messagebox.showwarning("Warning", "Please enter an application name")
                return
            
            def execute():
                result = self.run_async(open_app_with_url, app_name, url)
                if result:
                    self.apps_output.insert(tk.END, f"🚀 {result}\n")
                    self.apps_output.see(tk.END)
            
            threading.Thread(target=execute).start()
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Open", command=open_app).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
    
    # Preferences tab methods
    def set_preference(self):
        category = self.pref_category_var.get().strip()
        key = self.pref_key_var.get().strip()
        value = self.pref_value_var.get().strip()
        
        if not all([category, key, value]):
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        
        def execute():
            result = self.run_async(set_user_preference, category, key, value)
            if result:
                self.pref_output.insert(tk.END, f"✓ {result}\n")
                self.pref_output.see(tk.END)
                # Clear the fields
                self.pref_category_var.set("")
                self.pref_key_var.set("")
                self.pref_value_var.set("")
        
        threading.Thread(target=execute).start()
    
    def get_preference(self):
        category = self.get_category_var.get().strip()
        key = self.get_key_var.get().strip()
        
        if not all([category, key]):
            messagebox.showwarning("Warning", "Please fill in category and key")
            return
        
        def execute():
            result = self.run_async(get_user_preference, category, key)
            if result:
                self.pref_output.insert(tk.END, f"📋 {result}\n")
                self.pref_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    def list_preferences(self):
        def execute():
            result = self.run_async(list_user_preferences)
            if result:
                self.pref_output.insert(tk.END, f"📋 All Preferences:\n{result}\n\n")
                self.pref_output.see(tk.END)
        
        threading.Thread(target=execute).start()
    
    # Command tab methods
    def execute_command(self):
        command = self.command_var.get().strip()
        if not command:
            messagebox.showwarning("Warning", "Please enter a command")
            return
        
        def execute():
            result = self.run_async(run_command, command)
            if result:
                self.cmd_output.insert(tk.END, f"💻 {result}\n\n")
                self.cmd_output.see(tk.END)
                self.command_var.set("")
        
        threading.Thread(target=execute).start()
    
    def quick_command(self, command):
        self.command_var.set(command)
        self.execute_command()

def main():
    root = tk.Tk()
    app = MCPServerGUI(root)
    
    # Handle window close
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
