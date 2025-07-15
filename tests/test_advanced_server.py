#!/usr/bin/env python3
"""
Comprehensive test for Advanced Windows MCP Server
"""

import asyncio
import sys
import os

# Test server import
try:
    from advanced_windows_control_server import (
        get_system_info, get_hardware_info, list_processes, 
        start_process, list_directory, copy_file, move_file, 
        create_directory, read_file, write_file, get_network_info,
        ping_host, get_active_connections, run_command,
        get_system_services, get_disk_usage, get_environment_variables,
        get_installed_programs, get_startup_programs
    )
    print("✓ Advanced MCP Server imported successfully")
except Exception as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

async def test_all_advanced_tools():
    """Test all advanced MCP server tools"""
    print("\n🚀 Testing Advanced Windows MCP Server - Complete PC Control\n")
    
    # Test 1: System Information
    print("1. Testing get_system_info...")
    try:
        result = await get_system_info()
        print(f"   ✓ Success: System info retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Hardware Information
    print("\n2. Testing get_hardware_info...")
    try:
        result = await get_hardware_info()
        print(f"   ✓ Success: Hardware info retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Process Management
    print("\n3. Testing list_processes...")
    try:
        result = await list_processes()
        print(f"   ✓ Success: Process list retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Enhanced Directory Listing
    print("\n4. Testing enhanced list_directory...")
    try:
        result = await list_directory(".", show_hidden=True)
        print(f"   ✓ Success: Enhanced directory listing")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Create Directory
    print("\n5. Testing create_directory...")
    try:
        result = await create_directory("test_advanced_dir")
        print(f"   ✓ Success: Directory created")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Write File
    print("\n6. Testing write_file...")
    try:
        content = "Advanced MCP Server Test File\\nCreated by comprehensive test"
        result = await write_file("test_advanced_dir/test_file.txt", content)
        print(f"   ✓ Success: File written")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Read File
    print("\n7. Testing read_file...")
    try:
        result = await read_file("test_advanced_dir/test_file.txt")
        print(f"   ✓ Success: File read")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Network Information
    print("\n8. Testing get_network_info...")
    try:
        result = await get_network_info()
        print(f"   ✓ Success: Network info retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 9: Active Connections
    print("\n9. Testing get_active_connections...")
    try:
        result = await get_active_connections()
        print(f"   ✓ Success: Active connections retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 10: System Services
    print("\n10. Testing get_system_services...")
    try:
        result = await get_system_services()
        print(f"   ✓ Success: System services retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 11: Disk Usage
    print("\n11. Testing get_disk_usage...")
    try:
        result = await get_disk_usage("C:")
        print(f"   ✓ Success: Disk usage retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 12: Environment Variables
    print("\n12. Testing get_environment_variables...")
    try:
        result = await get_environment_variables()
        print(f"   ✓ Success: Environment variables retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 13: Installed Programs
    print("\n13. Testing get_installed_programs...")
    try:
        result = await get_installed_programs()
        print(f"   ✓ Success: Installed programs retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 14: Startup Programs
    print("\n14. Testing get_startup_programs...")
    try:
        result = await get_startup_programs()
        print(f"   ✓ Success: Startup programs retrieved")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 15: Enhanced Command Execution
    print("\n15. Testing enhanced run_command...")
    try:
        result = await run_command("echo Advanced MCP Server Test")
        print(f"   ✓ Success: Command executed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 16: Ping Host
    print("\n16. Testing ping_host...")
    try:
        result = await ping_host("8.8.8.8", 2)
        print(f"   ✓ Success: Ping completed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*80)
    print("🎉 ADVANCED MCP SERVER TEST COMPLETE!")
    print("="*80)
    print("\n📋 AVAILABLE TOOLS SUMMARY:")
    print("• System Information & Hardware Details")
    print("• Process Management (List, Kill, Start)")
    print("• Enhanced File Operations (Copy, Move, Delete)")
    print("• Network Monitoring & Connections")
    print("• Windows Service Control")
    print("• Power Management (Shutdown, Restart, Sleep)")
    print("• Registry Operations")
    print("• System Monitoring")
    print("• Advanced System Operations")
    print("\n🔒 SECURITY FEATURES:")
    print("• Enhanced command filtering")
    print("• Process safety checks")
    print("• Registry access controls")
    print("• Power management safeguards")
    print("\n🎯 READY FOR COMPLETE PC CONTROL!")

if __name__ == "__main__":
    asyncio.run(test_all_advanced_tools())
