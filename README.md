# MCP Windows Automation Server

A comprehensive Model Context Protocol (MCP) server for Windows automation, providing AI assistants with the ability to control Windows applications, system settings, and perform various automation tasks.

## Features

- **System Information**: Get detailed Windows system information, installed programs, running processes
- **Window Management**: Focus, minimize, maximize windows, get window lists
- **Mouse & Keyboard Control**: Click, drag, type, keyboard shortcuts
- **Application Automation**: Control specific applications like Spotify, Notepad, Calculator
- **Web Automation**: Browser automation with Selenium WebDriver
- **Screen Capture**: Take screenshots and find images on screen
- **Music Control**: Comprehensive Spotify automation and music playlist management
- **User Preferences**: Store and retrieve user preferences
- **System Monitoring**: Monitor system activity and performance

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/mcp-windows-automation.git
cd mcp-windows-automation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. For web automation, install ChromeDriver:
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Place it in your PATH or in the project directory

## Usage

### Running the MCP Server

```bash
python src/unified_server.py
```

### Configuration

Edit the configuration files in the `config/` directory:
- `claude_desktop_config.json` - Claude Desktop integration
- `user_preferences.json` - User preferences storage

### Example Usage

```python
# Example of using the automation server
from src.unified_server import AutomationServer

server = AutomationServer()
# The server will be available via MCP protocol
```

## Project Structure

```
├── src/                    # Source code
│   ├── unified_server.py           # Main MCP server
│   ├── advanced_automation_server.py  # Advanced automation features
│   ├── mcp_gui.py                 # GUI interface
│   └── ...
├── tests/                  # Test files
├── docs/                   # Documentation
├── examples/               # Example scripts and configurations
├── config/                 # Configuration files
└── README.md
```

## Documentation

- [Advanced Automation Documentation](docs/ADVANCED_AUTOMATION_DOCUMENTATION.md)
- [MCP Server Setup Guide](docs/MCP_SERVER_SETUP_COMPLETE.md)
- [Natural Language Guide](docs/NATURAL_LANGUAGE_GUIDE.md)
- [Advanced PC Control](docs/ADVANCED_PC_CONTROL_COMPLETE.md)
- [MCP GUI Documentation](docs/MCP_GUI_DOCUMENTATION.md)

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Requirements

- Python 3.7+
- Windows 10/11
- Required Python packages (see requirements.txt)
- ChromeDriver for web automation features

## Support

For issues and questions, please open an issue on GitHub.
