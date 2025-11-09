# 🚀 MCP Windows Server - AI-Powered Windows Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)
[![PyPI version](https://badge.fury.io/py/mcp-windows-server.svg)](https://badge.fury.io/py/mcp-windows-server)
[![AI Ready](https://img.shields.io/badge/AI-Assistant%20Ready-brightgreen.svg)](https://github.com/Mahipal/mcp-windows-server)

> **Transform your Windows PC into an intelligent automation hub controlled by AI assistants like Claude, ChatGPT, and more.**

## 🔍 Overview

**MCP Windows Server** is an AI-native automation framework that enables AI assistants to control Windows systems through natural language commands. Built on the **Model Context Protocol (MCP)**, it provides secure, comprehensive system-level automation capabilities.

### 🤖 What is Model Context Protocol (MCP)?

MCP is an open protocol by Anthropic that allows AI models to interact safely with local tools, APIs, and system services. Our server implements this protocol for Windows, making AI assistants powerful desktop automation agents.

- 🔐 **Secure System Access** - Controlled command execution with safety filters
- 🧠 **AI Agent Compatible** - Works with Claude, ChatGPT, and other AI assistants  
- 🔄 **Real-Time Communication** - Instant bidirectional AI ↔️ System interaction
- 🔧 **Plugin Architecture** - Extensible framework for custom automation

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install mcp-windows-server

# Or install from source
git clone https://github.com/mukul975/mcp-windows-automation.git
cd mcp-windows-server
pip install -r requirements.txt
```

### Usage

```bash
# Start the MCP server
mcp-windows-server

# Or use the unified server directly
unified-server
```

### Claude Desktop Integration

1. Install the package: `pip install mcp-windows-server`
2. Configure Claude Desktop:

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

3. Restart Claude Desktop and start automating!

## 🌟 Key Features

- ✅ **200+ Automation Tools** - Comprehensive Windows control
- 🧠 **AI-Context Aware** - Understands natural language commands
- 🔁 **Bidirectional Communication** - Real-time AI ↔️ System interaction
- ⚙️ **Safe Execution** - Built-in command filtering and validation
- 🧱 **Modular Design** - Plugin-based architecture
- 🧪 **ML Integration** - Machine learning for predictive automation

## 🧭 Automation Categories

| Category | Description | Examples |
|----------|-------------|----------|
| 🖥️ **System Control** | Process, registry, services management | Kill processes, manage services, registry edits |
| 📁 **File Operations** | File system automation | Copy, move, search, backup files |
| 🌐 **Web Automation** | Browser control and web scraping | Form filling, data extraction, navigation |
| 🖼️ **Image Processing** | Screenshot and image manipulation | OCR, image editing, screen capture |
| 📊 **Data Analysis** | ML training and data processing | Model training, data visualization |
| 🏢 **Office Integration** | Microsoft Office automation | Excel reports, Word documents, PowerPoint |
| 🔒 **Security** | System security and monitoring | Firewall rules, security scans, monitoring |
| 🌐 **Network** | Network configuration and monitoring | WiFi management, network diagnostics |

## 🛠️ Example Commands

Once integrated with Claude Desktop, you can use natural language:

```
"Take a screenshot and save it as desktop.png"
"Get my system information"
"List all running processes"
"Create a backup of my Documents folder"
"Check my network connection status"
"Open Calculator application"
```

## 📁 Project Structure

```
mcp-windows-server/
├── mcp_windows_automation/     # Main package
│   └── __init__.py
├── unified_server.py           # Core MCP server
├── office_mcp_server.py        # Office integration
├── config/                     # Configuration templates
├── docs/                       # Documentation
├── examples/                   # Usage examples
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Optional MySQL database integration
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Python configuration
PYTHONPATH=/path/to/mcp-windows-server
PYTHONUNBUFFERED=1
```

### Advanced Configuration

For advanced setups, copy the configuration template:

```bash
cp config/claude_desktop_config.template.json config/claude_desktop_config.json
# Edit with your specific paths and credentials
```

## 🧪 Development

### Running from Source

```bash
git clone https://github.com/Mahipal/mcp-windows-server.git
cd mcp-windows-server
pip install -r requirements.txt
python unified_server.py
```

### Building Package

```bash
python -m build
pip install dist/mcp_windows_server-*.whl
```

## 🔒 Security

- **Command Filtering**: Dangerous commands are blocked by default
- **Safe Execution**: All operations run in controlled environment
- **No Credential Storage**: Sensitive data excluded from package
- **Template-Based Config**: Only safe configuration templates included

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

- **Author**: Mahipal
- **Email**: mukuljangra5@gmail.com
- **GitHub**: [Mahipal](https://github.com/Mahipal)
- **PyPI**: [mcp-windows-server](https://pypi.org/project/mcp-windows-server/)

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for the Model Context Protocol
- [Claude](https://claude.ai/) for AI assistant integration
- The open-source community for inspiration and contributions

---

> **"Automate Everything. With AI."** 🧠💻

*Made with ❤️ for the AI automation community*
