#!/usr/bin/env python3
"""
MCP Windows Automation Server Launcher

This script launches the unified MCP server from the src directory.
It can be used as an alternative entry point for the MCP server.
"""

import sys
import os
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Add the src directory to the Python path
    src_dir = script_dir / "src"
    sys.path.insert(0, str(src_dir))
    
    # Change to the project directory
    os.chdir(script_dir)
    
    try:
        # Import and run the unified server
        import unified_server
        # The server will run automatically when imported since it has mcp.run() at the end
        print("MCP server is running...")
    except ImportError as e:
        print(f"Error importing unified_server: {e}")
        print(f"Make sure unified_server.py exists in: {src_dir}")
        sys.exit(1)
    except Exception as e:
        print(f"Error running MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
