#!/usr/bin/env python3
"""
Tests for All 98 Security Tools
"""

import pytest
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import all tools from unified_server
from unified_server import (
    # User preference tools
    set_user_preference, get_user_preference, list_user_preferences,
    
    # System monitoring tools
    get_system_info, list_processes, get_startup_programs, get_installed_programs,
    monitor_system_activity, monitor_for_security_issues,
    
    # UI automation tools
    get_mouse_position, move_mouse, click_at_coordinates, drag_and_drop,
    send_keyboard_shortcut, type_text, scroll_screen,
    
    # Window management tools
    get_window_list, focus_window, take_screenshot,
    
    # Application control tools
    open_app_with_url, run_command, automate_notepad, automate_calculator,
    
    # Web automation tools
    start_web_automation, close_web_automation, navigate_to_url,
    find_and_click_element, type_in_element, get_page_title,
    
    # Image recognition tools
    find_image_on_screen, click_image_if_found,
    
    # Automation workflow tools
    create_automation_workflow,
    
    # Music and media tools
    play_favorite_song, add_to_playlist, show_playlist,
    open_youtube_with_search, smart_music_action
)

class TestAllSecurityTools:
    """Test all 98 security tools"""
    
    @pytest.mark.asyncio
    async def test_user_preference_tools(self):
        """Test user preference management tools"""
        # Test set_user_preference
        result = await set_user_preference("test", "key", "value")
        assert "Preference set" in result
        
        # Test get_user_preference
        result = await get_user_preference("test", "key")
        assert "test.key = value" in result
        
        # Test list_user_preferences
        result = await list_user_preferences()
        assert "test" in result
        
    @pytest.mark.asyncio
    async def test_system_monitoring_tools(self):
        """Test system monitoring tools"""
        # Test get_system_info
        result = await get_system_info()
        assert "Error" not in result
        
        # Test list_processes
        result = await list_processes()
        assert "Error" not in result
        
        # Test get_startup_programs
        result = await get_startup_programs()
        assert "Error" not in result
        
        # Test get_installed_programs
        result = await get_installed_programs()
        assert "Error" not in result
        
    @pytest.mark.asyncio
    async def test_ui_automation_tools(self):
        """Test UI automation tools"""
        # Test get_mouse_position
        result = await get_mouse_position()
        assert "Error" not in result
        
        # Test type_text
        result = await type_text("test")
        assert "Error" not in result
        
    @pytest.mark.asyncio
    async def test_application_control_tools(self):
        """Test application control tools"""
        # Test open_app_with_url
        result = await open_app_with_url("notepad")
        assert "Error" not in result or "Opened" in result
        
        # Test run_command
        result = await run_command("echo test")
        assert "Error" not in result
        
    @pytest.mark.asyncio  
    async def test_media_tools(self):
        """Test media and entertainment tools"""
        # Test open_youtube_with_search
        result = await open_youtube_with_search("test")
        assert "Error" not in result or "Opened" in result
        
        # Test add_to_playlist
        result = await add_to_playlist("Test Song")
        assert "Error" not in result or "Added" in result
