@echo off
echo Starting continuous security monitoring...
echo This will run every 30 minutes. Press Ctrl+C to stop.
cd /d "D:\mcpdocs\mcpwindows"
python continuous_monitor.py
