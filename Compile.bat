@echo off
TITLE ChocolateyUpdate Compiler
python -V > NUL 2> NUL
IF errorlevel 1 ECHO PYTHON NOT IN PATH! && PAUSE && EXIT
CD %~dp0
python -m pip install -U pyinstaller
python -m pip install -r %~dp0requirements.txt
pyinstaller -F -i choco.ico --clean ChocolateyUpdate.py
RMDIR /S /Q build __pycache__
DEL /q ChocolateyUpdate.spec
ECHO Done! File is located in %~dp0dist
PAUSE
EXIT
