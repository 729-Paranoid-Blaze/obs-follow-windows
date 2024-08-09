# Follow Windows
My first GitHub project!

A script to update OBS sources to move to where their corresponding window is.
This script currently only works in Windows (the operating system).
This script functions similar to: https://github.com/henke37/window-follower, but it supports newer versions of OBS as it is a script, not a plugin.

## How to use:
1) Download this script (Code -> Download ZIP).
2) Install a version of python that is compatible with OBS, and make sure that you add python.exe to PATH.
3) Install modules that this script needs:

Command line:
```commandline
cd /path/to/folder/you/downloaded
```
```commandline
pip install -r requirements.txt
```
4) Open OBS and go to Tools -> Scripts.
5) In "Python Settings," find the folder where python is installed, e.g. Python312 (or whatever version of python that you installed)
6) In "Scripts," add this script (obs-follow-windows.py) with the "+" button.
7) Enter the names of the windows that you want OBS to follow, separated by a comma, e.g. "Minecraft, Google Chrome".

This script updates the position of the sources corresponding to these window names based on the position of the windows.
Both window captures and game captures can be followed.
8) If you want to keep the sources within the boundaries of your screen, tick the checkbox.

## Useful information
Some windows change their name. To make this script follow these windows despite their name changing, the name that you enter into
OBS can be shortened to be part of both the original name and the new name for the window. For example, if you are following
Google Chrome, you can enter "Google Chrome" instead of "New Tab - Google Chrome", so that even when you change tabs, the script will still follow Chrome.
If the names that you enter are too ambiguous, the program will not follow anything. For example, if 2 windows of Chrome are open, and 
you entered "Google Chrome", the script will not know which window to follow, so it will not follow anything. 


If you add another source through OBS, you can press the refresh script arrow in OBS to update the dropdown list of window names.

## Why I made this
Because I needed to follow some windows while using the newest version of OBS.

Tested OBS versions: 30.2.2

## Credits
Made by me with a little help from Mr. GPT.
