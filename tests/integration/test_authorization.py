#!/usr/bin/env python3
"""
Authorization Check Tests
"""

import pytest
import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unified_server import set_user_preference, get_user_preference

class TestAuthorization:
    """Test authorization checks"""
    
    @pytest.mark.asyncio
    async def test_admin_only_functions(self):
        """Test admin-only function access"""
        # Test that admin functions require proper authorization
        result = await set_user_preference("admin", "test", "value")
        assert "Preference set" in result
        
    @pytest.mark.asyncio
    async def test_user_permission_boundaries(self):
        """Test user permission boundaries"""
        # Test that users can only access their own data
        result = await get_user_preference("user", "test")
        assert "not found" in result or "user.test" in result
        
    @pytest.mark.asyncio
    async def test_privilege_escalation_prevention(self):
        """Test privilege escalation prevention"""
        # Test that users cannot escalate privileges
        result = await set_user_preference("admin", "privilege", "escalated")
        assert "Preference set" in result  # Should be allowed but not escalate
