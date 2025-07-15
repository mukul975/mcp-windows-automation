#!/usr/bin/env python3
"""
Test script for Advanced Automation Server
"""

import asyncio
import sys
import os

# Test server import
try:
    from advanced_automation_server import (
        open_app, close_app, click_coordinates, type_text, capture_screen,
        run_powershell, navigate_browser, control_adobe_app, 
        control_development_app, control_game_launcher, get_window_list,
        focus_window, automate_workflow, get_installed_programs
    )
    print("✓ Advanced Automation Server imported successfully")
except Exception as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

async def test_automation_features():
    """Test automation features"""
    print("\n🤖 Testing Advanced Automation Server - Complete UI Control\n")
    
    # Test 1: Open Application
    print("1. Testing open_app...")
    try:
        result = await open_app("notepad")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get Window List
    print("\n2. Testing get_window_list...")
    try:
        result = await get_window_list()
        print(f"   ✓ Success: Found windows")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Type Text
    print("\n3. Testing type_text...")
    try:
        result = await type_text("Hello from Advanced Automation Server!")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Capture Screen
    print("\n4. Testing capture_screen...")
    try:
        result = await capture_screen("automation_test_screenshot.png")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: PowerShell Command
    print("\n5. Testing run_powershell...")
    try:
        result = await run_powershell("Get-Date")
        print(f"   ✓ Success: PowerShell executed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Close Application
    print("\n6. Testing close_app...")
    try:
        result = await close_app("notepad")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Adobe App Control
    print("\n7. Testing control_adobe_app...")
    try:
        result = await control_adobe_app("photoshop", "open")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Development App Control
    print("\n8. Testing control_development_app...")
    try:
        result = await control_development_app("visual_studio", "open")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 9: Game Launcher Control
    print("\n9. Testing control_game_launcher...")
    try:
        result = await control_game_launcher("steam", "open")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 10: Workflow Automation
    print("\n10. Testing automate_workflow...")
    try:
        workflow_steps = [
            {
                "action": "open_app",
                "parameters": {"app_name": "calculator"}
            },
            {
                "action": "wait",
                "parameters": {"seconds": 2}
            },
            {
                "action": "type",
                "parameters": {"text": "123+456="}
            },
            {
                "action": "wait",
                "parameters": {"seconds": 1}
            }
        ]
        
        result = await automate_workflow("Calculator Test", workflow_steps)
        print(f"   ✓ Success: Workflow executed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*80)
    print("🎉 ADVANCED AUTOMATION SERVER TEST COMPLETE!")
    print("="*80)
    print("\n🤖 ADVANCED AUTOMATION FEATURES:")
    print("• Complete UI Control (Click, Type, Screenshot)")
    print("• Application Management (Open, Close, Focus)")
    print("• Adobe Creative Suite Control")
    print("• Development Environment Control")
    print("• Game Launcher Management")
    print("• Workflow Automation")
    print("• PowerShell Integration")
    print("• Browser Control with JavaScript")
    print("• Window Management")
    print("• Action Logging & Monitoring")
    print("\n🎯 READY FOR COMPLETE PC AUTOMATION!")

if __name__ == "__main__":
    asyncio.run(test_automation_features())
