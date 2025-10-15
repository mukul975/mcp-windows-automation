"""
MCP Windows Automation Package

A comprehensive Windows automation framework using Model Context Protocol (MCP).
Provides AI-powered system control, file operations, process management, and more.
"""

__version__ = "1.0.1"
__author__ = "Mahipal"
__email__ = "mukuljangra5@gmail.com"

# Import main function from unified_server
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from unified_server import main
except ImportError:
    def main():
        """Fallback main function if unified_server is not available."""
        print("Error: unified_server module not found. Please ensure unified_server.py is in the project root.")
        sys.exit(1)

__all__ = ["main"]