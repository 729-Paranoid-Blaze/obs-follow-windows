# Follow Windows
My first GitHub project!

A script to update OBS sources to move to where their corresponding window is on the screen.
This script currently only works in Windows (the operating system).
This script functions similar to: https://github.com/henke37/window-follower, but it supports newer versions of OBS as it is a script, not a plugin.

## How to use:
1) Download this script (code -> download script).
2) Install a version of python compatible with OBS.
3) To install modules that this script needs:
```bash
pip install -r requirements.txt
```
4) Open OBS and go to Tools -> Scripts, and add this script (obs-follow-windows.py) with the "+" button.
5) Enter the names of the windows that you want OBS to follow, separated by a comma, e.g. "Minecraft, Google Chrome".

This script updates the position of the sources corresponding to these window names based on the position of the windows.
Both window captures and game captures can be followed.

5) Choose if you want to keep windows within the boundaries of your screen or not.

## Useful information
Some windows change their name. To make this script follow these windows despite their name changing, the name that you enter into
OBS can be shortened to be part of both the original name and the new name for the window. For example, if you are following
Google Chrome, you can enter "Google Chrome" instead of "New Tab - Google Chrome", so that even when you change tabs, the script will still follow Chrome.

If you add another source through OBS, you can press the refresh script arrow in OBS to update the dropdown list of window names.

## Why I made this
Because I needed to follow some windows while using the newest version of OBS.

Tested versions of OBS: 30.2.2
