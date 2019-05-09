# V1.0
# https://github.com/Technetium1
# Licensed under The Unlicense [unlicense.org]
from os import system
from shutil import which
from pathlib import Path
from requests import get
import sys
import ctypes


def printascii():
    system('cls')
    system('title Tech\'s Chocolate Updater')
    print(r"""
.---..-- .- .  .\\ ,-.    .- .  . .-.  .- .-. .   .. .---..--.   .  .  . .-. .-.  .. .---..--.-.
  |  |  /   |  |  (   `  /   |  |/   \/  /   \|  /  \  |  |   \ /   |  | |  )|  \/  \  |  |  |  )
  |  |- |   |--|   `-.   |   |--||   ||  |   ||  |--|  |  |-   Y    |  | |-' |  ||--|  |  |- |-<
  |  |  \   |  |  .   )  \   |  |\   /\  \   /|  |  |  |  |    |    |  | |   |  /|  |  |  |  |  \
  '  '-- `- '  '   `-'    `- '  ' '-'  `- `-' `--'  '  '  `--  '    `--` '   '-' '  '  '  '--'   '
          """)
    print('\n')


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
    r = get(packagesurl, allow_redirects=True)
    open('ChocolateyPackages.txt', 'wb').write(r.content)
    system('pause')
    exit(1)


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
    if ctypes.windll.shell32.IsUserAnAdmin():
        printascii()
        if which("choco") is not None:
            checkforpackages()
        else:
            print("NO CHOCOLATEY INSTALLED!")
            installchoco = "start /wait powershell.exe Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
            system(installchoco)
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, sys.argv[0], None, 1)
    else:
        printascii()
        print("ATTEMPTING TO GET ADMINISTRATOR PERMISSIONS!")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, sys.argv[0], None, 1)


admincheck()
