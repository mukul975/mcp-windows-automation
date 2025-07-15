# 🎯 Natural Language Command Guide

## 🎵 **"Open Chrome and Play YouTube with My Favorite Song"**

### ✅ **NOW FULLY SUPPORTED!**

Your enhanced MCP server can now handle complex natural language requests like:
- "Open Chrome and play YouTube with my favorite song"
- "Play my favorite music on YouTube"
- "Open YouTube and search for my favorite song"

---

## 🚀 **How It Works**

### **Step 1: Set Your Preferences**
```
User: "Set my favorite song to Shape of You by Ed Sheeran"
```
**Server Response:** `set_user_preference('music', 'favorite_song', 'Shape of You by Ed Sheeran')`

### **Step 2: Natural Language Request**
```
User: "Open Chrome and play YouTube with my favorite song"
```
**Server Actions:**
1. `play_favorite_song()` - Retrieves your favorite song
2. `open_youtube_with_search('Shape of You by Ed Sheeran')` - Opens YouTube with search
3. **Result:** Chrome opens with YouTube searching for your favorite song

---

## 🎵 **Music Command Examples**

### **Basic Commands:**
- **"Play my favorite song"** → `play_favorite_song()`
- **"Open YouTube"** → `open_app_with_url('chrome', 'https://www.youtube.com')`
- **"Search YouTube for [song name]"** → `open_youtube_with_search('song name')`

### **Smart Commands:**
- **"Open Chrome and play YouTube with my favorite song"** → `smart_open_command('youtube', 'favorite song')`
- **"Play music"** → `smart_music_action('play_favorite')`
- **"Open YouTube Music"** → `smart_music_action('open_youtube_music')`
- **"Play random song from my playlist"** → `smart_music_action('random_song')`

### **Playlist Management:**
- **"Add [song name] to my playlist"** → `add_to_playlist('song name')`
- **"Show my playlist"** → `show_playlist()`
- **"Play a random song from my playlist"** → `smart_music_action('random_song')`

---

## 🎯 **Complete Setup Example**

### **1. Initial Setup:**
```
User: "Set up my music preferences"
Claude: Let me help you set up your music preferences.

User: "Set my favorite song to Blinding Lights by The Weeknd"
Server: set_user_preference('music', 'favorite_song', 'Blinding Lights by The Weeknd')
Result: ✓ Preference set: music.favorite_song = Blinding Lights by The Weeknd

User: "Add Shape of You by Ed Sheeran to my playlist"
Server: add_to_playlist('Shape of You by Ed Sheeran')
Result: ✓ Added 'Shape of You by Ed Sheeran' to your playlist
```

### **2. Natural Language Usage:**
```
User: "Open Chrome and play YouTube with my favorite song"
Server: 
1. play_favorite_song() → Gets "Blinding Lights by The Weeknd"
2. open_youtube_with_search('Blinding Lights by The Weeknd')
Result: ✓ Chrome opens with YouTube searching for "Blinding Lights by The Weeknd"
```

---

## 📱 **Application Commands**

### **Smart App Opening:**
- **"Open Chrome"** → `open_app_with_url('chrome')`
- **"Open Chrome with YouTube"** → `open_app_with_url('chrome', 'https://www.youtube.com')`
- **"Open Spotify"** → `open_app_with_url('spotify')`
- **"Open calculator"** → `open_app_with_url('calculator')`

### **Context-Aware Commands:**
- **"Open YouTube with music"** → Opens YouTube Music
- **"Open Facebook"** → `smart_open_command('facebook')`
- **"Open Twitter"** → `smart_open_command('twitter')`

---

## 🎼 **Music Service Integration**

### **YouTube:**
- **"Open YouTube"** → Regular YouTube
- **"Open YouTube Music"** → YouTube Music service
- **"Search YouTube for [song]"** → YouTube search results

### **Other Services:**
- **"Open Spotify"** → Spotify app
- **"Open Pandora"** → Pandora web player
- **"Open music service"** → Default music preference

---

## 🔧 **Advanced Features**

### **Preference Management:**
- **"Show my preferences"** → `list_user_preferences()`
- **"What's my favorite song?"** → `get_user_preference('music', 'favorite_song')`
- **"Show my playlist"** → `show_playlist()`

### **Smart Automation:**
- **"Play my favorite song"** → Auto-detects and plays
- **"Play random music"** → Selects from your playlist
- **"Open my music"** → Context-aware music opening

---

## 🎯 **Example Conversation Flow**

```
User: "I want to listen to music"
Claude: I can help you with that! Let me open your music options.

User: "Open Chrome and play YouTube with my favorite song"
Claude: I'll open Chrome and play your favorite song on YouTube.
[Executes: play_favorite_song() → opens YouTube with search]

User: "Actually, play something random from my playlist"
Claude: Let me play a random song from your playlist.
[Executes: smart_music_action('random_song')]

User: "Add this new song to my playlist"
Claude: What song would you like to add?

User: "Add Watermelon Sugar by Harry Styles"
Claude: [Executes: add_to_playlist('Watermelon Sugar by Harry Styles')]
✓ Added 'Watermelon Sugar by Harry Styles' to your playlist
```

---

## 🛠️ **Available Tools for Natural Language**

### **🎵 Music Tools:**
- `play_favorite_song()` - Play user's favorite song
- `open_youtube_with_search(query)` - YouTube search
- `smart_music_action(action)` - Smart music actions
- `add_to_playlist(song)` - Add to playlist
- `show_playlist()` - Show current playlist

### **📱 App Tools:**
- `open_app_with_url(app, url)` - Open apps with URLs
- `smart_open_command(service, params)` - Context-aware opening

### **⚙️ Preference Tools:**
- `set_user_preference(category, key, value)` - Set preferences
- `get_user_preference(category, key)` - Get preferences
- `list_user_preferences()` - List all preferences

---

## 🎉 **SUCCESS: Natural Language Fully Supported!**

Your request **"Open Chrome and play YouTube with my favorite song"** is now fully supported with:

✅ **User preference management**  
✅ **Smart YouTube integration**  
✅ **Chrome automation**  
✅ **Favorite song storage**  
✅ **Playlist management**  
✅ **Context-aware commands**  
✅ **Natural language processing**  

**Your PC now understands and executes complex natural language commands!** 🎯

---

*Enhanced Automation Server - Natural Language Command System*  
*Status: Fully Operational ✅*  
*Natural Language Support: Complete 🎵*  
*User Preferences: Enabled 🎯*
