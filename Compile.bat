@echo off
TITLE ChocolateyUpdate Compiler
python -V > NUL 2> NUL
if errorlevel 1 echo PYTHON NOT IN PATH! && PAUSE && EXIT
cd %~dp0
pyinstaller -F -i choco.ico --clean ChocolateyUpdate.py
pause
exit
