@echo off

pip install -r requirements.txt

pyinstaller --onefile --windowed --name NetworkMonitor network_monitor_full.py

pause
