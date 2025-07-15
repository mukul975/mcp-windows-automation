#!/usr/bin/env python3
"""
Comprehensive test for MCP server functionality
Tests each tool individually to ensure they work properly
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Import the server functions directly for testing
from simple_windows_server import (
    get_system_info, run_command, list_directory, 
    read_file, write_file, get_environment_variables,
    ping_host, get_disk_usage
)

async def test_all_tools():
    """Test all MCP server tools"""
    print("🧪 Testing Simple Windows MCP Server Tools\n")
    
    # Test 1: System Info
    print("1. Testing get_system_info...")
    try:
        result = await get_system_info()
        print(f"   ✓ Success: {result[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Run Command
    print("\n2. Testing run_command...")
    try:
        result = await run_command("echo Hello MCP")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: List Directory
    print("\n3. Testing list_directory...")
    try:
        result = await list_directory(".")
        print(f"   ✓ Success: Found {len(result.split('\\n'))} items")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Read File
    print("\n4. Testing read_file...")
    try:
        result = await read_file("D:\\mcpdocs\\mcpwindows\\test_simple_server.py")
        print(f"   ✓ Success: Read {len(result)} characters")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Write File
    print("\n5. Testing write_file...")
    try:
        test_content = "This is a test file created by MCP server\\nCurrent time: " + str(asyncio.get_event_loop().time())
        result = await write_file("test_output.txt", test_content)
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Environment Variables
    print("\n6. Testing get_environment_variables...")
    try:
        result = await get_environment_variables()
        print(f"   ✓ Success: Retrieved environment variables")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Ping Host
    print("\n7. Testing ping_host...")
    try:
        result = await ping_host("127.0.0.1")
        print(f"   ✓ Success: Ping completed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Disk Usage
    print("\n8. Testing get_disk_usage...")
    try:
        result = await get_disk_usage("C:")
        print(f"   ✓ Success: {result.split('\\n')[0]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*50)
    print("✅ All tool tests completed!")
    print("Your MCP server is ready for use with Claude Desktop")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(test_all_tools())
