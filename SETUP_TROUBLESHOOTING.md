# MCP Server Setup and Troubleshooting Guide

## Quick Fix for "No such file or directory" Error

If you're getting the error:
```
python: can't open file 'D:\mcpdocs\mcpwindows\unified_server.py': [Errno 2] No such file or directory
```

This is because the file has been moved to the `src/` directory during project restructuring.

## Solution Options

### Option 1: Update Claude Desktop Configuration (Recommended)

Update your Claude Desktop configuration file to point to the correct path:

**Location:** `%AppData%\Claude\claude_desktop_config.json`

**Updated Configuration:**
```json
{
  "mcpServers": {
    "unified-server": {
      "command": "python",
      "args": ["D:\\mcpdocs\\mcpwindows\\src\\unified_server.py"],
      "cwd": "D:\\mcpdocs\\mcpwindows"
    }
  }
}
```

### Option 2: Use the Launcher Script

Use the provided launcher script in the root directory:

```json
{
  "mcpServers": {
    "unified-server": {
      "command": "python",
      "args": ["D:\\mcpdocs\\mcpwindows\\run_mcp_server.py"],
      "cwd": "D:\\mcpdocs\\mcpwindows"
    }
  }
}
```

### Option 3: Manual Testing

Test the server manually from the command line:

```bash
# Navigate to the project directory
cd D:\mcpdocs\mcpwindows

# Run the server directly
python src/unified_server.py

# Or use the launcher
python run_mcp_server.py
```

## Project Structure

After restructuring, the project layout is:

```
D:\mcpdocs\mcpwindows\
├── src/                          # Source code files
│   ├── unified_server.py         # Main MCP server (moved here)
│   ├── advanced_automation_server.py
│   ├── mcp_gui.py
│   └── ...
├── tests/                        # Test files
├── docs/                         # Documentation
├── examples/                     # Example configurations
├── config/                       # Configuration files
│   ├── claude_desktop_config.json
│   └── claude_desktop_config_alternative.json
├── run_mcp_server.py            # Launcher script
├── README.md
└── requirements.txt
```

## Dependencies

Make sure you have all required dependencies installed:

```bash
pip install -r requirements.txt
```

Key dependencies include:
- `mcp` - Model Context Protocol library
- `pyautogui` - GUI automation
- `pywin32` - Windows API access
- `psutil` - System information
- `selenium` - Web automation
- `opencv-python` - Computer vision

## Common Issues and Solutions

### 1. "UI automation libraries not available"

**Problem:** Missing PyAutoGUI or related libraries

**Solution:**
```bash
pip install pyautogui pygetwindow requests websocket-client
```

### 2. "ModuleNotFoundError: No module named 'mcp'"

**Problem:** MCP library not installed

**Solution:**
```bash
pip install mcp
```

### 3. "ImportError: No module named 'cv2'"

**Problem:** OpenCV not installed

**Solution:**
```bash
pip install opencv-python
```

### 4. ChromeDriver Issues

**Problem:** Web automation not working

**Solution:**
1. Download ChromeDriver from https://chromedriver.chromium.org/
2. Place it in your PATH or project directory
3. Or install automatically: `pip install webdriver-manager`

## Server Status Check

To verify the server is working correctly:

```bash
# Check if server starts without errors
python src/unified_server.py

# Check UI automation status
python -c "import pyautogui; print(f'PyAutoGUI: {pyautogui.__version__}')"

# Check MCP library
python -c "import mcp; print('MCP library installed')"
```

## Configuration Files

### Claude Desktop Config
- **Location:** `%AppData%\Claude\claude_desktop_config.json`
- **Alternative:** Use the provided config files in the `config/` directory

### User Preferences
- **Location:** `user_preferences.json` (created automatically)
- **Purpose:** Stores user settings like favorite songs, playlists, etc.

## Logging and Debugging

MCP server logs are typically located at:
```
C:\Users\{username}\AppData\Local\warp\Warp\data\logs\mcp\
```

To debug issues:
1. Check the MCP logs for specific error messages
2. Test individual components manually
3. Verify all dependencies are installed
4. Check file paths and permissions

## Testing the Setup

After configuration, test with these commands in Claude Desktop:

1. **Basic System Info:**
   - "Get system information"
   - "List running processes"

2. **UI Automation:**
   - "Take a screenshot"
   - "Open calculator"

3. **Music Integration:**
   - "Play favorite song"
   - "Add song to playlist"

4. **Web Automation:**
   - "Open YouTube"
   - "Search for videos"

## Support

If you continue to have issues:
1. Check the GitHub repository for updates
2. Review the MCP logs for specific error messages
3. Ensure all file paths are correct in your configuration
4. Verify Python version compatibility (Python 3.7+ required)

## Advanced Configuration

For advanced users, you can customize:
- Server timeout settings
- UI automation delays
- Web automation browser options
- Custom keyboard shortcuts
- Application-specific automation rules

See the individual server files in `src/` for detailed configuration options.
