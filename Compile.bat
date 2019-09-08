@echo off
TITLE ChocolateyUpdate Compiler
python -V > NUL 2> NUL
if errorlevel 1 echo PYTHON NOT IN PATH! && PAUSE && EXIT
cd %~dp0
python -m pip install -U pyinstaller
python -m pip install -r %~dp0requirements.txt
pyinstaller -F -i choco.ico --clean ChocolateyUpdate.py
ECHO Done! File is located in %~dp0dist
pause
exit
