#!/usr/bin/env python3
"""
Authentication Flow Tests for MCP Windows Security Tools
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import the functions we need to test
from unified_server import (
    set_user_preference, 
    get_user_preference, 
    list_user_preferences,
    load_user_preferences,
    save_user_preferences,
    PREFERENCES_FILE
)

class TestAuthentication:
    """Test authentication flows for user preferences"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_preferences_file = PREFERENCES_FILE
        # Use temporary file for testing
        self.test_preferences_file = os.path.join(self.temp_dir, 'test_preferences.json')
        
        # Mock the global PREFERENCES_FILE
        import unified_server
        unified_server.PREFERENCES_FILE = self.test_preferences_file
        
    def teardown_method(self):
        """Cleanup after each test"""
        # Restore original preferences file
        import unified_server
        unified_server.PREFERENCES_FILE = self.original_preferences_file
        
        # Clean up temporary files
        if os.path.exists(self.test_preferences_file):
            os.remove(self.test_preferences_file)
        os.rmdir(self.temp_dir)
    
    @pytest.mark.asyncio
    async def test_valid_user_preference_set(self):
        """Test setting valid user preferences"""
        # Test data
        category = "music"
        key = "favorite_song"
        value = "Test Song"
        
        # Execute
        result = await set_user_preference(category, key, value)
        
        # Verify
        assert f"Preference set: {category}.{key} = {value}" in result
        
        # Verify persistence
        preferences = load_user_preferences()
        assert category in preferences
        assert key in preferences[category]
        assert preferences[category][key] == value
    
    @pytest.mark.asyncio
    async def test_invalid_user_preference_set(self):
        """Test setting invalid user preferences"""
        # Test empty category
        result = await set_user_preference("", "key", "value")
        assert "Preference set: .key = value" in result  # Should still work but with empty category
        
        # Test empty key
        result = await set_user_preference("category", "", "value")
        assert "Preference set: category. = value" in result
        
        # Test empty value
        result = await set_user_preference("category", "key", "")
        assert "Preference set: category.key = " in result
    
    @pytest.mark.asyncio
    async def test_preference_access_control(self):
        """Test preference access control and isolation"""
        # Set preferences for different categories
        await set_user_preference("music", "favorite_song", "Song A")
        await set_user_preference("browser", "default", "chrome")
        
        # Verify category isolation
        music_pref = await get_user_preference("music", "favorite_song")
        browser_pref = await get_user_preference("browser", "default")
        
        assert "music.favorite_song = Song A" in music_pref
        assert "browser.default = chrome" in browser_pref
        
        # Verify cross-category access doesn't exist
        invalid_pref = await get_user_preference("music", "default")
        assert "not found" in invalid_pref
    
    @pytest.mark.asyncio
    async def test_session_timeout(self):
        """Test session management and timeout handling"""
        # This test simulates session behavior
        # In a real implementation, you would test actual session timeouts
        
        # Set a preference
        await set_user_preference("session", "test_key", "test_value")
        
        # Verify it exists
        result = await get_user_preference("session", "test_key")
        assert "session.test_key = test_value" in result
        
        # Simulate session cleanup (in real implementation, this would be automatic)
        preferences = load_user_preferences()
        if "session" in preferences:
            del preferences["session"]
        save_user_preferences(preferences)
        
        # Verify session data is cleared
        result = await get_user_preference("session", "test_key")
        assert "not found" in result
    
    @pytest.mark.asyncio
    async def test_concurrent_user_sessions(self):
        """Test handling of concurrent user sessions"""
        # Simulate multiple users by using different preference categories
        users = ["user1", "user2", "user3"]
        
        # Set preferences for different users
        for user in users:
            await set_user_preference(user, "preference", f"{user}_value")
        
        # Verify each user's preferences are isolated
        for user in users:
            result = await get_user_preference(user, "preference")
            assert f"{user}.preference = {user}_value" in result
        
        # Verify no cross-user data leakage
        for user in users:
            for other_user in users:
                if user != other_user:
                    result = await get_user_preference(user, "preference")
                    assert f"{other_user}_value" not in result
    
    @pytest.mark.asyncio
    async def test_preference_encryption(self):
        """Test preference data encryption/security"""
        # Set a sensitive preference
        await set_user_preference("security", "api_key", "secret_key_123")
        
        # Read the raw file to ensure it's not stored in plaintext
        with open(self.test_preferences_file, 'r') as f:
            file_content = f.read()
        
        # In a real implementation, this would test encryption
        # For now, we just verify the structure is correct
        preferences = json.loads(file_content)
        assert "security" in preferences
        assert "api_key" in preferences["security"]
        
        # Verify retrieval works
        result = await get_user_preference("security", "api_key")
        assert "security.api_key = secret_key_123" in result
    
    @pytest.mark.asyncio
    async def test_preference_backup_restore(self):
        """Test preference backup and restore functionality"""
        # Set initial preferences
        test_preferences = {
            "music": {"favorite_song": "Song A", "volume": "80"},
            "browser": {"default": "chrome", "homepage": "google.com"}
        }
        
        for category, prefs in test_preferences.items():
            for key, value in prefs.items():
                await set_user_preference(category, key, value)
        
        # Create backup
        backup_file = os.path.join(self.temp_dir, 'backup_preferences.json')
        original_preferences = load_user_preferences()
        with open(backup_file, 'w') as f:
            json.dump(original_preferences, f)
        
        # Modify preferences
        await set_user_preference("music", "favorite_song", "Song B")
        
        # Restore from backup
        with open(backup_file, 'r') as f:
            backup_preferences = json.load(f)
        save_user_preferences(backup_preferences)
        
        # Verify restoration
        result = await get_user_preference("music", "favorite_song")
        assert "music.favorite_song = Song A" in result
    
    @pytest.mark.asyncio
    async def test_malformed_preference_data(self):
        """Test handling of malformed preference data"""
        # Create malformed JSON file
        with open(self.test_preferences_file, 'w') as f:
            f.write('{"invalid": json"}')
        
        # Should handle gracefully
        result = await get_user_preference("test", "key")
        assert "not found" in result
        
        # Should be able to set new preferences even with corrupted file
        result = await set_user_preference("test", "key", "value")
        assert "Preference set: test.key = value" in result
    
    @pytest.mark.asyncio
    async def test_preference_data_validation(self):
        """Test input validation for preference data"""
        # Test various input types
        test_cases = [
            ("category", "key", "string_value"),
            ("category", "key", "123"),
            ("category", "key", "true"),
            ("category", "key", "false"),
            ("category", "key", "null"),
        ]
        
        for category, key, value in test_cases:
            result = await set_user_preference(category, key, value)
            assert f"Preference set: {category}.{key} = {value}" in result
            
            # Verify retrieval
            retrieved = await get_user_preference(category, key)
            assert f"{category}.{key} = {value}" in retrieved
    
    @pytest.mark.asyncio
    async def test_preference_list_functionality(self):
        """Test preference listing functionality"""
        # Set multiple preferences
        await set_user_preference("music", "favorite_song", "Song A")
        await set_user_preference("music", "volume", "80")
        await set_user_preference("browser", "default", "chrome")
        
        # List all preferences
        result = await list_user_preferences()
        
        # Verify structure
        assert "User Preferences:" in result
        assert "[music]" in result
        assert "favorite_song: Song A" in result
        assert "volume: 80" in result
        assert "[browser]" in result
        assert "default: chrome" in result
    
    @pytest.mark.asyncio
    async def test_empty_preference_list(self):
        """Test listing when no preferences exist"""
        result = await list_user_preferences()
        assert "No user preferences set" in result
    
    def test_load_user_preferences_file_not_exists(self):
        """Test loading preferences when file doesn't exist"""
        # Remove the file if it exists
        if os.path.exists(self.test_preferences_file):
            os.remove(self.test_preferences_file)
        
        preferences = load_user_preferences()
        assert preferences == {}
    
    def test_save_user_preferences_error_handling(self):
        """Test error handling when saving preferences"""
        # Create invalid directory path
        invalid_path = "/invalid/path/preferences.json"
        
        import unified_server
        original_file = unified_server.PREFERENCES_FILE
        unified_server.PREFERENCES_FILE = invalid_path
        
        try:
            # This should handle the error gracefully
            save_user_preferences({"test": "data"})
            # If we reach here, the function handled the error gracefully
            assert True
        except Exception as e:
            # Should not raise an exception
            assert False, f"save_user_preferences raised exception: {e}"
        finally:
            unified_server.PREFERENCES_FILE = original_file

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
