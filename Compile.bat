@echo off
pyinstaller -F -i choco.ico --clean ChocolateyUpdate.py
pause
exit