#!/usr/bin/env python3
"""
Release script for MCP Windows Automation package.

This script automates the process of building, testing, and releasing the package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result

def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning build artifacts...")
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            else:
                path.unlink()
                print(f"Removed file: {path}")

def check_dependencies():
    """Check if required build dependencies are installed."""
    print("🔍 Checking build dependencies...")
    required_packages = ["build", "twine", "wheel"]
    missing_packages = []
    
    for package in required_packages:
        result = run_command(f"python -m pip show {package}", check=False)
        if result.returncode != 0:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        run_command(f"python -m pip install {' '.join(missing_packages)}")

def run_tests():
    """Run tests if they exist."""
    print("🧪 Running tests...")
    if Path("tests").exists():
        run_command("python -m pytest tests/ -v")
    else:
        print("No tests directory found, skipping tests")

def build_package():
    """Build the package."""
    print("📦 Building package...")
    run_command("python -m build")

def check_package():
    """Check the built package."""
    print("✅ Checking package...")
    dist_files = list(Path("dist").glob("*.tar.gz")) + list(Path("dist").glob("*.whl"))
    for dist_file in dist_files:
        run_command(f"python -m twine check {dist_file}")

def upload_to_testpypi():
    """Upload to Test PyPI."""
    print("🚀 Uploading to Test PyPI...")
    run_command("python -m twine upload --repository testpypi dist/*")

def upload_to_pypi():
    """Upload to PyPI."""
    print("🚀 Uploading to PyPI...")
    run_command("python -m twine upload dist/*")

def main():
    """Main release process."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Release MCP Windows Automation package")
    parser.add_argument("--test", action="store_true", help="Upload to Test PyPI instead of PyPI")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-upload", action="store_true", help="Skip uploading (build only)")
    parser.add_argument("--clean-only", action="store_true", help="Only clean build artifacts")
    
    args = parser.parse_args()
    
    if args.clean_only:
        clean_build()
        return
    
    print("🚀 Starting release process for MCP Windows Automation...")
    
    # Step 1: Clean previous builds
    clean_build()
    
    # Step 2: Check dependencies
    check_dependencies()
    
    # Step 3: Run tests (optional)
    if not args.skip_tests:
        run_tests()
    
    # Step 4: Build package
    build_package()
    
    # Step 5: Check package
    check_package()
    
    # Step 6: Upload (optional)
    if not args.skip_upload:
        if args.test:
            upload_to_testpypi()
        else:
            confirm = input("Upload to PyPI? This cannot be undone! (y/N): ")
            if confirm.lower() == 'y':
                upload_to_pypi()
            else:
                print("Upload cancelled. Package built successfully in dist/")
    
    print("✅ Release process completed!")
    print("\nNext steps:")
    print("1. Test the package: pip install mcpwindows")
    print("2. Verify installation: mcpwindows --help")
    print("3. Update version in pyproject.toml for next release")

if __name__ == "__main__":
    main()