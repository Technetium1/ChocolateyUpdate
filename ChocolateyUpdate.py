# https://github.com/Technetium1
# Licensed under The Unlicense [unlicense.org]
from os import system
from os import remove
from os import rename
from shutil import which
from pathlib import Path
from ctypes import windll
import urllib3
import json
import certifi
import sys

version = "2.2"


def printascii():
    system("cls")
    system("title Tech\'s Chocolatey Updater V" + version)
    print(r"""
.---..-- .- .  .\\ ,-.    .- .  . .-.  .- .-. .   .. .---..--.   .  .  . .-. .-.  .. .---..--.-.
  |  |  /   |  |  (   `  /   |  |/   \/  /   \|  /  \  |  |   \ /   |  | |  )|  \/  \  |  |  |  )
  |  |- |   |--|   `-.   |   |--||   ||  |   ||  |--|  |  |-   Y    |  | |-' |  ||--|  |  |- |-<
  |  |  \   |  |  .   )  \   |  |\   /\  \   /|  |  |  |  |    |    |  | |   |  /|  |  |  |  |  \
  '  '-- `- '  '   `-'    `- '  ' '-'  `- `-' `--'  '  '  `--  '    `--` '   '-' '  '  '  '--'   '
          """)
    print("\n" + "v" + version + "\n")


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
    packagesurl = "https://raw.githubusercontent.com/Technetium1/ChocolateyUpdate/master/ChocolateyPackages.txt"
    http = urllib3.PoolManager(ca_certs=certifi.where())
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = http.request(
        "GET",
        packagesurl,
        timeout=urllib3.Timeout(connect=15.0, read=15.0),
        retries=4,
        redirect=False)
    with open("ChocolateyPackages.txt", "wb") as chocopkgs:
        chocopkgs.write(r.data)
    system("pause")
    raise SystemExit


def installpackages():
    with open("ChocolateyPackages.txt", "r") as file:
        updates = file.read().replace("\n", " ")
    print("FOUND PACKAGES: " + updates)
    up = "choco upgrade -y "
    print("\n\n\n~~~~~~~~~~~~~~~~~~~~\nUPDATING CHOCOLATEY!\n~~~~~~~~~~~~~~~~~~~~\n\n\n")
    system(up + "chocolatey")
    print("\n\n\n~~~~~~~~~~~~~~~~~~\nUPDATING PACKAGES!\n~~~~~~~~~~~~~~~~~~\n\n\n")
    system(up + updates)
    print("\nSUCCESS!\n")
    system("pause")


def checkforpackages():
    if Path("ChocolateyPackages.txt").exists():
        installpackages()
    else:
        nopackagefile()


def admincheck():
    if windll.shell32.IsUserAnAdmin():
        printascii()
        stopcontrolledfolderaccess = "powershell.exe -Command Set-MpPreference -EnableControlledFolderAccess Disabled > nul 2>&1"
        system(stopcontrolledfolderaccess)
        if Path("OldChocolateyUpdate.exe").exists():
            remove("OldChocolateyUpdate.exe")
        if getattr(sys, "frozen", True):
            selfupdate()
        if which("choco") is not None:
            checkforpackages()
        else:
            print("NO CHOCOLATEY INSTALLED!")
            installchoco = "start /wait powershell.exe Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
            system(installchoco)
            print("\nPlease restart the program!\n")
            system("pause")
            raise SystemExit
    else:
        printascii()
        print("ATTEMPTING TO GET ADMINISTRATOR PERMISSIONS!")
        windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, sys.argv[0], None, 1)


def selfupdate():
    updateurl = "https://api.github.com/repos/Technetium1/ChocolateyUpdate/releases/latest"
    http = urllib3.PoolManager(ca_certs=certifi.where())
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = http.request(
        "GET",
        updateurl,
        headers={"User-Agent": "curl", "Accept": "application/vnd.github.v3+json"},
        timeout=urllib3.Timeout(connect=6.0, read=6.0),
        retries=4,
        redirect=False)
    updateresult = json.loads(r.data.decode("utf-8"))
    currentversion = updateresult["tag_name"]
    downloadlink = updateresult["assets"][0]["browser_download_url"]
    if currentversion > version:
        print("\nNewer version found on GitHub!\n")
    elif currentversion < version:
        print("\nVersion newer than what was found on GitHub!\n")
    elif currentversion == version:
        print("\nAlready at latest GitHub release!\n")
    else:
        print("\nSomething went wrong checking for updates! If this continues report to https://github.com/Technetium1/ChocolateyUpdate\n")
        system("pause")
        raise SystemExit
    if updateresult["assets"] and currentversion > version:
        print("Downloading new release from: " + downloadlink)
        if Path("NewChocolateyUpdate.exe").exists():
            remove("NewChocolateyUpdate.exe")
        if Path("OldChocolateyUpdate.exe").exists():
            remove("OldChocolateyUpdate.exe")
        r = http.request(
            "GET",
            downloadlink,
            headers={"User-Agent": "curl"},
            timeout=urllib3.Timeout(connect=10.0, read=120.0),
            retries=2,
            redirect=True)
        with open("NewChocolateyUpdate.exe", "wb") as downloadedfile:
            downloadedfile.write(r.data)
        rename("ChocolateyUpdate.exe", "OldChocolateyUpdate.exe")
        system("attrib +h OldChocolateyUpdate.exe")
        rename("NewChocolateyUpdate.exe", "ChocolateyUpdate.exe")
        print("Update completed! Restart ChocolateyUpdate to complete!")
        system("pause")
        raise SystemExit
    else:
        pass


admincheck()
