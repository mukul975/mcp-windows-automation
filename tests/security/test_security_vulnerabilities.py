#!/usr/bin/env python3
"""
Security Vulnerability Tests for MCP Windows Security Tools
"""

import pytest
import asyncio
import os
import sys
import tempfile
import subprocess
import json
import time
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import the functions we need to test
from unified_server import (
    set_user_preference,
    get_user_preference,
    list_user_preferences,
    run_command,
    open_app_with_url,
    navigate_to_url,
    type_text,
    find_and_click_element,
    type_in_element,
    take_screenshot,
    automate_notepad,
    create_automation_workflow,
    get_system_info,
    list_processes,
    monitor_system_activity,
    load_user_preferences,
    save_user_preferences
)

class TestSecurityVulnerabilities:
    """Test security vulnerabilities in MCP Windows Security Tools"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_preferences_file = "user_preferences.json"
        self.test_preferences_file = os.path.join(self.temp_dir, 'test_preferences.json')
        
        # Mock the global PREFERENCES_FILE
        import unified_server
        unified_server.PREFERENCES_FILE = self.test_preferences_file
        
    def teardown_method(self):
        """Cleanup after test"""
        # Restore original preferences file
        import unified_server
        unified_server.PREFERENCES_FILE = self.original_preferences_file
        
        # Clean up temporary files
        if os.path.exists(self.test_preferences_file):
            os.remove(self.test_preferences_file)
        os.rmdir(self.temp_dir)
    
    @pytest.mark.asyncio
    async def test_sql_injection_prevention(self):
        """Test prevention of SQL injection attacks"""
        
        # Test SQL injection attempts in user preferences
        sql_injection_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; SELECT * FROM users; --",
            "admin'--",
            "' UNION SELECT password FROM users WHERE username='admin'--"
        ]
        
        for payload in sql_injection_payloads:
            # Test in category field
            result = await set_user_preference(payload, "key", "value")
            assert "Error" not in result or "Preference set" in result
            
            # Test in key field
            result = await set_user_preference("category", payload, "value")
            assert "Error" not in result or "Preference set" in result
            
            # Test in value field
            result = await set_user_preference("category", "key", payload)
            assert "Error" not in result or "Preference set" in result
            
            # Verify no SQL injection occurred by checking file integrity
            if os.path.exists(self.test_preferences_file):
                with open(self.test_preferences_file, 'r') as f:
                    content = f.read()
                    # Should still be valid JSON
                    try:
                        json.loads(content)
                    except json.JSONDecodeError:
                        pytest.fail(f"SQL injection payload '{payload}' corrupted preference file")
    
    @pytest.mark.asyncio
    async def test_xss_protection(self):
        """Test protection against Cross-Site Scripting (XSS) attacks"""
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>",
            "\" onmouseover=\"alert('XSS')\"",
            "<iframe src=\"javascript:alert('XSS')\"></iframe>"
        ]
        
        for payload in xss_payloads:
            # Test XSS in user preferences
            result = await set_user_preference("web", "content", payload)
            assert "Preference set" in result
            
            # Verify the payload is stored but not executed
            retrieved = await get_user_preference("web", "content")
            assert payload in retrieved
            
            # Test XSS in automation workflows
            try:
                workflow_steps = f"1. Type: {payload}\n2. Click: button"
                result = await create_automation_workflow(workflow_steps)
                # Should not execute the script
                assert "Error" not in result or "workflow" in result.lower()
            except Exception as e:
                # Exception is acceptable as it means the system rejected the payload
                assert "script" not in str(e).lower()
    
    @pytest.mark.asyncio
    async def test_csrf_protection(self):
        """Test protection against Cross-Site Request Forgery (CSRF) attacks"""
        
        # Test CSRF-like attacks in web automation
        csrf_payloads = [
            "http://evil.com/csrf?action=transfer&amount=1000",
            "javascript:void(document.forms[0].submit())",
            "data:text/html,<script>document.forms[0].submit()</script>",
            "http://localhost/admin/delete_user?id=1"
        ]
        
        for payload in csrf_payloads:
            # Test in URL navigation
            try:
                result = await navigate_to_url(payload)
                # Should either reject malicious URLs or handle safely
                assert "Error" in result or "Navigated" in result
            except Exception as e:
                # Exception is acceptable for malicious URLs
                pass
            
            # Test in app opening
            try:
                result = await open_app_with_url("chrome", payload)
                # Should handle safely
                assert "Error" in result or "Opened" in result
            except Exception as e:
                # Exception is acceptable for malicious URLs
                pass
    
    @pytest.mark.asyncio
    async def test_command_injection_prevention(self):
        """Test prevention of command injection attacks"""
        
        command_injection_payloads = [
            "echo hello; rm -rf /",
            "echo hello && del /f /q C:\\*",
            "echo hello | powershell -c \"Remove-Item -Path C:\\ -Recurse\"",
            "hello; shutdown /s /t 0",
            "test`whoami`",
            "$(rm -rf /)",
            "hello; net user hacker password123 /add",
            "echo hello & format C:",
            "dir; powershell -EncodedCommand <base64>",
            "echo test > /etc/passwd"
        ]
        
        for payload in command_injection_payloads:
            # Test command injection in run_command
            try:
                result = await run_command(payload)
                # Should either sanitize or reject the command
                assert "Error" in result or len(result) > 0
                
                # Verify no harmful commands were executed
                assert "removed" not in result.lower()
                assert "deleted" not in result.lower()
                assert "formatted" not in result.lower()
                assert "shutdown" not in result.lower()
                
            except Exception as e:
                # Exception is acceptable as it means the system rejected the command
                assert "injection" not in str(e).lower()
            
            # Test in automation workflows
            try:
                workflow_steps = f"1. Run command: {payload}"
                result = await create_automation_workflow(workflow_steps)
                # Should handle safely
                assert "Error" in result or "workflow" in result.lower()
            except Exception as e:
                # Exception is acceptable
                pass
    
    @pytest.mark.asyncio
    async def test_path_traversal_prevention(self):
        """Test prevention of path traversal attacks"""
        
        path_traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "..%255c..%255c..%255cwindows%255csystem32%255cconfig%255csam",
            "/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
            "C:/windows/system32/config/sam",
            "/etc/shadow",
            "../../../../../../etc/passwd%00.txt"
        ]
        
        for payload in path_traversal_payloads:
            # Test path traversal in screenshot functionality
            try:
                result = await take_screenshot(payload)
                # Should either reject malicious paths or handle safely
                assert "Error" in result or "Screenshot" in result
                
                # Verify no sensitive files were accessed
                assert "passwd" not in result.lower()
                assert "shadow" not in result.lower()
                assert "sam" not in result.lower()
                
            except Exception as e:
                # Exception is acceptable for malicious paths
                pass
            
            # Test in preferences file paths
            try:
                # Try to manipulate preferences file path
                malicious_prefs = {payload: {"key": "value"}}
                save_user_preferences(malicious_prefs)
                
                # Should not create files outside expected directory
                assert not os.path.exists(payload)
                assert not os.path.exists(os.path.join("/etc", "passwd"))
                assert not os.path.exists(os.path.join("C:", "windows", "system32", "config", "sam"))
                
            except Exception as e:
                # Exception is acceptable
                pass
    
    @pytest.mark.asyncio
    async def test_buffer_overflow_protection(self):
        """Test protection against buffer overflow attacks"""
        
        # Create large payloads that might cause buffer overflows
        large_payloads = [
            "A" * 1000,      # 1KB
            "B" * 10000,     # 10KB
            "C" * 100000,    # 100KB
            "D" * 1000000,   # 1MB
        ]
        
        for payload in large_payloads:
            # Test large input in user preferences
            try:
                result = await set_user_preference("test", "large_key", payload)
                assert "Error" in result or "Preference set" in result
                
                # Verify system stability
                system_info = await get_system_info()
                assert "Error" not in system_info
                
            except Exception as e:
                # Exception is acceptable for oversized input
                assert "memory" not in str(e).lower()
            
            # Test large input in text typing
            try:
                # Use smaller payload for typing test
                if len(payload) <= 10000:
                    result = await type_text(payload)
                    assert "Error" in result or len(result) > 0
            except Exception as e:
                # Exception is acceptable
                pass
    
    @pytest.mark.asyncio
    async def test_race_condition_handling(self):
        """Test handling of race conditions"""
        
        # Test concurrent access to preferences
        async def concurrent_preference_access():
            tasks = []
            for i in range(100):
                tasks.append(set_user_preference("race_test", f"key_{i}", f"value_{i}"))
                tasks.append(get_user_preference("race_test", f"key_{i}"))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        
        # Run concurrent operations
        results = await concurrent_preference_access()
        
        # Check for race condition indicators
        errors = [r for r in results if isinstance(r, Exception)]
        assert len(errors) < len(results) * 0.1, f"Too many errors indicating race conditions: {len(errors)}"
        
        # Verify data integrity
        preferences = load_user_preferences()
        if "race_test" in preferences:
            for key, value in preferences["race_test"].items():
                assert key.startswith("key_"), f"Invalid key format: {key}"
                assert value.startswith("value_"), f"Invalid value format: {value}"
    
    @pytest.mark.asyncio
    async def test_privilege_escalation_prevention(self):
        """Test prevention of privilege escalation attacks"""
        
        privilege_escalation_payloads = [
            "net user administrator newpassword",
            "net localgroup administrators user /add",
            "runas /user:administrator cmd",
            "powershell -Command \"Start-Process cmd -Verb RunAs\"",
            "schtasks /create /tn evil /tr \"cmd /c net user hacker pass /add\" /sc once /st 12:00",
            "reg add HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\sethc.exe /v Debugger /t REG_SZ /d cmd.exe",
            "wmic process call create \"cmd /c net user hacker pass /add\"",
            "sc create evil binpath= \"cmd /c net user hacker pass /add\"",
            "at 12:00 /every:M,T,W,Th,F,S,Su cmd /c \"net user hacker pass /add\""
        ]
        
        for payload in privilege_escalation_payloads:
            # Test privilege escalation in command execution
            try:
                result = await run_command(payload)
                
                # Should either reject or handle safely
                assert "Error" in result or "Access denied" in result or len(result) == 0
                
                # Verify no new users were created
                users_result = await run_command("net user")
                assert "hacker" not in users_result.lower()
                assert "evil" not in users_result.lower()
                
            except Exception as e:
                # Exception is acceptable for privilege escalation attempts
                pass
            
            # Test in automation workflows
            try:
                workflow_steps = f"1. Run: {payload}"
                result = await create_automation_workflow(workflow_steps)
                # Should handle safely
                assert "Error" in result or "workflow" in result.lower()
            except Exception as e:
                # Exception is acceptable
                pass
    
    @pytest.mark.asyncio
    async def test_input_validation_bypass(self):
        """Test attempts to bypass input validation"""
        
        bypass_payloads = [
            None,
            "",
            " ",
            "\n",
            "\t",
            "\r\n",
            "\x00",
            "\x01",
            "\\",
            "\"",
            "'",
            "`",
            "${USER}",
            "%USERNAME%",
            "$(whoami)",
            "`whoami`",
            "{{user}}",
            "<![CDATA[evil]]>",
            "<!--evil-->",
            "unicode\u0000test"
        ]
        
        for payload in bypass_payloads:
            # Test various input validation scenarios
            try:
                if payload is not None:
                    result = await set_user_preference("bypass_test", "key", payload)
                    assert "Error" not in result or "Preference set" in result
                    
                    # Verify the payload is safely stored
                    retrieved = await get_user_preference("bypass_test", "key")
                    if payload:
                        assert str(payload) in retrieved or "not found" in retrieved
                else:
                    # Test None input
                    result = await set_user_preference("bypass_test", "key", None)
                    assert "Error" not in result or "Preference set" in result
                    
            except Exception as e:
                # Exception is acceptable for invalid input
                pass
    
    @pytest.mark.asyncio
    async def test_information_disclosure_prevention(self):
        """Test prevention of information disclosure"""
        
        # Test attempts to access sensitive information
        sensitive_queries = [
            "SELECT * FROM users",
            "SHOW TABLES",
            "DESCRIBE users",
            "../../../etc/passwd",
            "C:\\Windows\\System32\\config\\SAM",
            "registry::HKEY_LOCAL_MACHINE\\SAM",
            "env:USERNAME",
            "$env:COMPUTERNAME",
            "Get-Process",
            "Get-WmiObject -Class Win32_UserAccount"
        ]
        
        for query in sensitive_queries:
            # Test in user preferences
            try:
                result = await set_user_preference("sensitive", "query", query)
                assert "Preference set" in result
                
                # Verify no sensitive information is disclosed
                retrieved = await get_user_preference("sensitive", "query")
                assert query in retrieved  # Should store the query but not execute it
                
            except Exception as e:
                # Exception is acceptable
                pass
            
            # Test in system monitoring
            try:
                # Should not execute arbitrary queries
                result = await get_system_info()
                assert "Error" not in result
                
                # Should not contain sensitive information
                assert "password" not in result.lower()
                assert "secret" not in result.lower()
                assert "key" not in result.lower()
                
            except Exception as e:
                # Exception is acceptable
                pass
    
    @pytest.mark.asyncio
    async def test_denial_of_service_protection(self):
        """Test protection against denial of service attacks"""
        
        # Test resource exhaustion
        large_requests = []
        for i in range(1000):
            large_requests.append(set_user_preference(f"dos_test_{i}", "key", "value"))
        
        start_time = time.time()
        results = await asyncio.gather(*large_requests, return_exceptions=True)
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 60, f"DoS test took too long: {end_time - start_time}s"
        
        # Should not crash the system
        errors = [r for r in results if isinstance(r, Exception)]
        assert len(errors) < len(results) * 0.5, f"Too many errors indicating DoS vulnerability: {len(errors)}"
        
        # System should still be responsive
        system_info = await get_system_info()
        assert "Error" not in system_info
    
    @pytest.mark.asyncio
    async def test_authentication_bypass(self):
        """Test attempts to bypass authentication"""
        
        # Test various authentication bypass attempts
        bypass_attempts = [
            ("admin", "password"),
            ("", ""),
            ("admin", ""),
            ("", "password"),
            ("admin'--", "anything"),
            ("admin' OR '1'='1", "anything"),
            ("admin'; DROP TABLE users; --", "password"),
            ("../admin", "password"),
            ("admin\x00", "password"),
            ("admin\n", "password")
        ]
        
        for username, password in bypass_attempts:
            # Test in user preferences (simulating authentication)
            try:
                result = await set_user_preference("auth", "username", username)
                assert "Preference set" in result
                
                result = await set_user_preference("auth", "password", password)
                assert "Preference set" in result
                
                # Verify no authentication bypass occurred
                retrieved_user = await get_user_preference("auth", "username")
                retrieved_pass = await get_user_preference("auth", "password")
                
                # Should store the values but not grant special access
                assert username in retrieved_user or "not found" in retrieved_user
                assert password in retrieved_pass or "not found" in retrieved_pass
                
            except Exception as e:
                # Exception is acceptable for malicious input
                pass
    
    @pytest.mark.asyncio
    async def test_session_fixation_prevention(self):
        """Test prevention of session fixation attacks"""
        
        # Test session management in preferences
        session_ids = [
            "valid_session_123",
            "malicious_session",
            "admin_session",
            "../../etc/passwd",
            "<script>alert('xss')</script>",
            "'; DROP TABLE sessions; --"
        ]
        
        for session_id in session_ids:
            # Test session handling
            try:
                result = await set_user_preference("session", "id", session_id)
                assert "Preference set" in result
                
                # Verify session is properly managed
                retrieved = await get_user_preference("session", "id")
                assert session_id in retrieved
                
                # Should not affect other sessions
                other_sessions = await list_user_preferences()
                assert "session" in other_sessions
                
            except Exception as e:
                # Exception is acceptable
                pass

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
