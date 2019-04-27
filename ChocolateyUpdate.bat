@ECHO off
REM V1.0
REM https://github.com/Technetium1
REM Licensed under The Unlicense [unlicense.org]

TITLE Tech's Chocolatey Updater
CLS
ECHO ".---..-- .- .  .\\ ,-.    .- .  . .-.  .- .-. .   .. .---..--.   .  .  . .-. .-.  .. .---..--.-.  "
ECHO "  |  |  /   |  |  (   `  /   |  |/   \/  /   \|  /  \  |  |   \ /   |  | |  )|  \/  \  |  |  |  ) "
ECHO "  |  |- |   |--|   `-.   |   |--||   ||  |   ||  |--|  |  |-   Y    |  | |-' |  ||--|  |  |- |-<  "
ECHO "  |  |  \   |  |  .   )  \   |  |\   /\  \   /|  |  |  |  |    |    |  | |   |  /|  |  |  |  |  \ "
ECHO "  '  '-- `- '  '   `-'    `- '  ' '-'  `- `-' `--'  '  '  `--  '    `--` '   '-' '  '  '  '--'  ' "
CALL :AdminCheck

:AdminCheck
FLTMC >NUL 2>&1 && (
  CALL :ChocoCheck
) || (
  CALL :NoAdmin
)

:ChocoCheck
WHERE /q choco
IF ERRORLEVEL 1 (
  ECHO Chocolatey is not installed yet!
  @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
  ECHO Chocolatey is now installed, please close this window and rerun!
  PAUSE
  EXIT
) ELSE (
  CALL :Update
)

:CheckPackages
IF exist %~dp0ChocolateyPackages.txt ( set /p PKGLIST=<%~dp0ChocolateyPackages.txt ) ELSE ( powershell Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Technetium1/ChocolateyUpdate/master/ChocolateyPackages.txt' -OutFile %~dp0ChocolateyPackages.txt ; CALL :NoPackages)

:Update
ECHO Administrator check passed!
ECHO Updating Chocolatey!
ECHO .
ECHO .
ECHO .
ECHO .
choco upgrade -y chocolatey
ECHO Updating packages!
ECHO .
ECHO .
ECHO .
ECHO .
choco upgrade -y %PKGLIST%
ECHO .
ECHO .
ECHO .
ECHO .
ECHO DONE!
PAUSE
EXIT

:NoPackages
CLS
ECHO ######## ########  ########   #######  ########  ##
ECHO ##       ##     ## ##     ## ##     ## ##     ## ##
ECHO ##       ##     ## ##     ## ##     ## ##     ## ##
ECHO ######   ########  ########  ##     ## ########  ##
ECHO ##       ##   ##   ##   ##   ##     ## ##   ##   ##
ECHO ##       ##    ##  ##    ##  ##     ## ##    ## 
ECHO ######## ##     ## ##     ##  #######  ##     ## ##
ECHO.
ECHO ######## ERROR: NO PACKAGES FILE WAS FOUND! ########
ECHO This script needs a package list to work properly
ECHO Since it didn't exist the default was downloaded
ECHO Edit out any unwanted programs and then rerun
ECHO ####################################################
ECHO.
PAUSE
EXIT

:NoAdmin
CLS
ECHO ######## ########  ########   #######  ########  ##
ECHO ##       ##     ## ##     ## ##     ## ##     ## ##
ECHO ##       ##     ## ##     ## ##     ## ##     ## ##
ECHO ######   ########  ########  ##     ## ########  ##
ECHO ##       ##   ##   ##   ##   ##     ## ##   ##   ##
ECHO ##       ##    ##  ##    ##  ##     ## ##    ##
ECHO ######## ##     ## ##     ##  #######  ##     ## ##
ECHO.
ECHO ##### ERROR: ADMINISTRATOR PRIVILEGES REQUIRED! ####
ECHO Right click and select "Run As Administrator"!
ECHO ####################################################
ECHO.
PAUSE
EXIT
