# https://github.com/Technetium1
# Licensed under The Unlicense [unlicense.org]
from os import system
from shutil import which
from pathlib import Path
from ctypes import windll
import urllib3
import certifi
import sys

version = '1.4'


def printascii():
    system('cls')
    system('title Tech\'s Chocolatey Updater V' + version)
    print(r"""
.---..-- .- .  .\\ ,-.    .- .  . .-.  .- .-. .   .. .---..--.   .  .  . .-. .-.  .. .---..--.-.
  |  |  /   |  |  (   `  /   |  |/   \/  /   \|  /  \  |  |   \ /   |  | |  )|  \/  \  |  |  |  )
  |  |- |   |--|   `-.   |   |--||   ||  |   ||  |--|  |  |-   Y    |  | |-' |  ||--|  |  |- |-<
  |  |  \   |  |  .   )  \   |  |\   /\  \   /|  |  |  |  |    |    |  | |   |  /|  |  |  |  |  \
  '  '-- `- '  '   `-'    `- '  ' '-'  `- `-' `--'  '  '  `--  '    `--` '   '-' '  '  '  '--'   '
          """)
    print('\n' + 'V' + version + '\n')


def nopackagefile():
    print(r"""
####################################################

######## ########  ########   #######  ########  ##
##       ##     ## ##     ## ##     ## ##     ## ##
##       ##     ## ##     ## ##     ## ##     ## ##
######   ########  ########  ##     ## ########  ##
##       ##   ##   ##   ##   ##     ## ##   ##   ##
##       ##    ##  ##    ##  ##     ## ##    ##
######## ##     ## ##     ##  #######  ##     ## ##

######## ERROR: NO PACKAGES FILE WAS FOUND! ########
This script needs a package list to work properly
Since it didn't exist the default was downloaded!
Edit out any unwanted programs and then rerun!
####################################################
        """)
    packagesurl = 'https://raw.githubusercontent.com/Technetium1/ChocolateyUpdate/master/ChocolateyPackages.txt'
    http = urllib3.PoolManager(ca_certs=certifi.where())
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = http.request(
        'GET',
        packagesurl,
        timeout=urllib3.Timeout(connect=15.0, read=15.0),
        retries=4)
    with open('ChocolateyPackages.txt', 'wb') as chocopkgs:
        chocopkgs.write(r.data)
    system('pause')
    raise SystemExit


def installpackages():
    with open('ChocolateyPackages.txt', 'r') as file:
        updates = file.read().replace('\n', ' ')
    print("FOUND PACKAGES: " + updates)
    up = 'choco upgrade -y '
    print('\n\n\n~~~~~~~~~~~~~~~~~~~~\nUPDATING CHOCOLATEY!\n~~~~~~~~~~~~~~~~~~~~\n\n\n')
    system(up + 'chocolatey')
    print('\n\n\n~~~~~~~~~~~~~~~~~~\nUPDATING PACKAGES!\n~~~~~~~~~~~~~~~~~~\n\n\n')
    system(up + updates)
    print('\nSUCCESS!\n')
    system('pause')


def checkforpackages():
    if Path('ChocolateyPackages.txt').exists():
        installpackages()
    else:
        nopackagefile()


def admincheck():
    if windll.shell32.IsUserAnAdmin():
        printascii()
        stopcontrolledfolderaccess = "powershell.exe -Command Set-MpPreference -EnableControlledFolderAccess Disabled > nul 2>&1"
        system(stopcontrolledfolderaccess)
        if which("choco") is not None:
            checkforpackages()
        else:
            print("NO CHOCOLATEY INSTALLED!")
            installchoco = "start /wait powershell.exe Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
            system(installchoco)
            print('\nPlease restart the program!\n')
            system('pause')
            raise SystemExit
    else:
        printascii()
        print("ATTEMPTING TO GET ADMINISTRATOR PERMISSIONS!")
        windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, sys.argv[0], None, 1)


admincheck()
