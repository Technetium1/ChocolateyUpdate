@ECHO off
REM https://github.com/Technetium1
TITLE Tech's Chocolatey Updater
CALL :AdminCheck

:AdminCheck
fltmc >nul 2>&1 && (
  CALL :ChocoCheck
) || (
  CALL :NoAdmin
)

:ChocoCheck
where /q choco
IF ERRORLEVEL 1 (
  ECHO Chocolatey is not installed yet!
  @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
  ECHO Chocolatey is now installed, please close the window and rerun!
  PAUSE
  EXIT
) ELSE (
  CALL :Update
)

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
choco upgrade -y 7zip bleachbit bluegriffon borderlessgaming calibre ccleaner cdburnerxp chocolateygui coretemp cpu-z.install curl defraggler dotnet4.7 etcher everything f.lux firefox gpg4win hackfont hashcheck hexchat hourglass.install imageresizerapp imgburn iperf3 libreoffice-fresh mumble nmap notepadplusplus openssh opera osfmount pidgin pidgin-otr putty.install qbittorrent recuva sharex silverlight skype speccy sumatrapdf.install unifying vim vlc webtorrent-desktop wget windirstat youtube-dl youtube-dl-gui
ECHO .
ECHO .
ECHO .
ECHO .
ECHO DONE!
PAUSE
EXIT

:NoAdmin
ECHO ######## ########  ########   #######  ########  ##
ECHO ##       ##     ## ##     ## ##     ## ##     ## ##
ECHO ##       ##     ## ##     ## ##     ## ##     ## ##
ECHO ######   ########  ########  ##     ## ########  ##
ECHO ##       ##   ##   ##   ##   ##     ## ##   ##   ##
ECHO ##       ##    ##  ##    ##  ##     ## ##    ## 
ECHO ######## ##     ## ##     ##  #######  ##     ## ##
ECHO.
ECHO ####### ERROR: ADMINISTRATOR PRIVILEGES REQUIRED! #########
ECHO This script must be run as Administrator to work properly!  
ECHO Right click and select "Run As Administrator"!
ECHO ###########################################################
ECHO.
pause
EXIT
