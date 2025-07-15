#!/usr/bin/env python3
"""
Test the enhanced automation server capabilities
"""

import asyncio
import sys

# Test server import
try:
    from enhanced_automation_server import (
        set_user_preference, get_user_preference, list_user_preferences,
        open_youtube_with_search, play_favorite_song, open_app_with_url,
        smart_music_action, add_to_playlist, show_playlist,
        smart_open_command, quick_setup_favorites
    )
    print("✓ Enhanced Automation Server imported successfully")
except Exception as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

async def test_automation_features():
    """Test automation features"""
    print("\n🎵 Testing Enhanced Automation Features\n")
    
    # Test 1: Set favorite song
    print("1. Setting favorite song...")
    try:
        result = await set_user_preference('music', 'favorite_song', 'Shape of You by Ed Sheeran')
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get favorite song
    print("\n2. Getting favorite song...")
    try:
        result = await get_user_preference('music', 'favorite_song')
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Add to playlist
    print("\n3. Adding songs to playlist...")
    try:
        await add_to_playlist('Blinding Lights by The Weeknd')
        await add_to_playlist('Dance Monkey by Tones and I')
        result = await add_to_playlist('Watermelon Sugar by Harry Styles')
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Show playlist
    print("\n4. Showing playlist...")
    try:
        result = await show_playlist()
        print(f"   ✓ Success: \\n{result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: List all preferences
    print("\n5. Listing all preferences...")
    try:
        result = await list_user_preferences()
        print(f"   ✓ Success: \\n{result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Open YouTube with search
    print("\n6. Testing YouTube search (simulation)...")
    try:
        result = await open_youtube_with_search("Shape of You Ed Sheeran")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Smart music action
    print("\n7. Testing smart music action...")
    try:
        result = await smart_music_action("play_favorite")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Smart open command
    print("\n8. Testing smart open command...")
    try:
        result = await smart_open_command("youtube", "favorite song")
        print(f"   ✓ Success: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 9: Quick setup guide
    print("\n9. Showing quick setup guide...")
    try:
        result = await quick_setup_favorites()
        print(f"   ✓ Success: Setup guide available")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*80)
    print("🎉 ENHANCED AUTOMATION TEST COMPLETE!")
    print("="*80)
    print("\n🎵 NEW AUTOMATION FEATURES:")
    print("• User Preference Management")
    print("• Smart YouTube Integration")
    print("• Favorite Song Management")
    print("• Playlist Management")
    print("• Smart App Opening")
    print("• Context-Aware Commands")
    print("\n🎯 READY FOR NATURAL LANGUAGE COMMANDS!")

if __name__ == "__main__":
    asyncio.run(test_automation_features())
