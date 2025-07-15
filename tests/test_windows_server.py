#!/usr/bin/env python3
"""
Test script for Windows MCP Server
This script tests the basic functionality of the Windows MCP server
"""

import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_server():
    """Test the Windows MCP server functionality"""
    
    # Configure server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["D:\\mcpdocs\\mcpwindows\\windows_system_server.py"],
        cwd="D:\\mcpdocs\\mcpwindows"
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                print("✅ Connected to Windows MCP Server")
                
                # Test system info
                print("\n📊 Testing system_info...")
                result = await session.call_tool("system_info", {})
                print(f"System Info: {result.content[0].text}")
                
                # Test file operations - list directory
                print("\n📁 Testing file_operations - read directory...")
                result = await session.call_tool("file_operations", {
                    "action": "read",
                    "source": "D:\\mcpdocs\\mcpwindows\\MCP_SERVER_SETUP_COMPLETE.md"
                })
                print(f"File read result: {result.content[0].text[:200]}...")
                
                # Test network operations - ping
                print("\n🌐 Testing network_operations - ping...")
                result = await session.call_tool("network_operations", {
                    "action": "ping",
                    "target": "8.8.8.8"
                })
                print(f"Ping result: {result.content[0].text}")
                
                # Test process management - list processes
                print("\n🔄 Testing process_management - list processes...")
                result = await session.call_tool("process_management", {
                    "action": "list"
                })
                print(f"Process list: {result.content[0].text[:300]}...")
                
                print("\n✅ All tests completed successfully!")
                
    except Exception as e:
        print(f"❌ Error testing server: {e}")

if __name__ == "__main__":
    asyncio.run(test_server())
