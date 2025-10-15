# MCP Windows Automation - Release Guide

## 📦 Package Information

- **Package Name**: `mcp-windows-server`
- **Version**: 1.0.0
- **Python Requirements**: >=3.10
- **Platform**: Windows
- **License**: MIT

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install mcp-windows-server

# Or install from local build
pip install dist/mcp_windows_server-1.0.0-py3-none-any.whl
```

### Usage

#### As a Command Line Tool

```bash
# Start the MCP server
mcp-windows-server

# Or use the unified server directly
unified-server
```

#### As a Python Module

```python
from mcp_windows_automation import main

# Start the server
main()
```

#### With Claude Desktop

1. Install the package: `pip install mcp-windows-server`
2. Configure Claude Desktop with the installed package:

```json
{
  "mcpServers": {
    "mcp-windows-server": {
      "command": "mcp-windows-server",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## 🛠️ Development Setup

### Building from Source

```bash
# Clone the repository
git clone https://github.com/mukul975/mcp-windows-automation.git
cd mcp-windows-automation

# Install dependencies
pip install -r requirements.txt

# Install build tools
pip install build twine wheel

# Build the package
python -m build

# Install locally for testing
pip install dist/mcp_windows_automation-1.0.0-py3-none-any.whl
```

### Using the Release Script

```bash
# Build and test (no upload)
python release.py --skip-upload

# Build and upload to Test PyPI
python release.py --test

# Build and upload to PyPI (production)
python release.py
```

## 📋 Package Contents

### Core Modules

- **`unified_server.py`**: Main MCP server with comprehensive Windows automation
- **`office_mcp_server.py`**: Microsoft Office integration server
- **`mcp_windows_automation/`**: Package module with entry points

### Available Commands

After installation, these commands are available:

- **`mcp-windows-server`**: Main entry point (recommended)
- **`unified-server`**: Direct access to unified_server.py

### Features

- 🖥️ **System Control**: Process management, system info, performance monitoring
- 📁 **File Operations**: Read, write, search, and manage files and directories
- 🌐 **Web Automation**: Browser control with Selenium
- 🖼️ **Image Processing**: Screenshot capture and image manipulation
- 📊 **Data Analysis**: ML training, data processing with pandas/scikit-learn
- 🏢 **Office Integration**: Word, Excel, PowerPoint automation
- 🔒 **Security**: Safe command execution with filtering
- 📈 **Monitoring**: System performance and resource tracking

## 🔧 Configuration

### Environment Variables

```bash
# MySQL Database (optional)
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Python Configuration
PYTHONPATH=/path/to/mcp-windows-automation
PYTHONUNBUFFERED=1
```

### Claude Desktop Configuration

Create or update `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-windows-automation": {
      "command": "mcp-windows-server",
      "env": {
        "PYTHONUNBUFFERED": "1",
        "MYSQL_USER": "your_username",
        "MYSQL_PASSWORD": "your_password",
        "MYSQL_DATABASE": "your_database"
      }
    }
  }
}
```

## 🧪 Testing

### Verify Installation

```bash
# Check if package is installed
pip show mcp-windows-automation

# Test command availability
mcp-windows-server --help
unified-server --help

# Test import
python -c "from mcp_windows_automation import main; print('Import successful')"
```

### Test with Claude Desktop

1. Install and configure as above
2. Restart Claude Desktop
3. Test with a simple command: "Get my system information"

## 📚 Documentation

- **Main Documentation**: `/docs/` directory
- **API Reference**: Generated from docstrings
- **Examples**: `/examples/` directory
- **Configuration Guide**: `/config/README.md`

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Ensure Python >=3.10 and all dependencies installed
2. **Command Not Found**: Check if Scripts directory is in PATH
3. **Permission Denied**: Run as administrator for system operations
4. **MySQL Connection**: Verify database credentials and server status

### Debug Mode

```bash
# Enable verbose logging
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from mcp_windows_automation import main
main()
"
```

## 🔄 Updates

### Version Management

Update version in `pyproject.toml`:

```toml
[project]
version = "1.1.0"  # Update this
```

### Release Process

1. Update version number
2. Update CHANGELOG.md
3. Run tests: `python release.py --skip-upload`
4. Build and upload: `python release.py`

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs/` directory
- **Email**: mukuljangra5@gmail.com

---

**Happy Automating! 🚀**