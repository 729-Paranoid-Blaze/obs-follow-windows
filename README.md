# Follow Windows
A script to update OBS sources to move to where their corresponding window is on the screen.
This script currently only works in Windows (the operating system).
This script functions similar to: https://github.com/henke37/window-follower, but it supports newer versions of OBS as it is a script, not a plugin.

## How to use:
After downloading the script, open OBS and go to Tools -> Scripts, and add this script (obs-follow-windows.py) with the "+" button.
Enter the names of the windows that you want OBS to follow, seperated by a comma, e.g. "Minecraft, Google Chrome".
This program updates the position of the sources corresponding to these window names in the current scene in OBS based on the position of the windows.
Both window captures and game captures can be followed.

Some windows change their name. To make this script follow these windows despite their name changing, the name that you enter into
OBS can be shortened to be part of both the original name of the window and the new name for the window. For example, if you are following
Google Chrome, you can enter "Google Chrome" instead of "New Tab - Google Chrome", so that even when you change tabs, OBS will still follow Chrome.

If you add another source through OBS, you can press the refresh script arrow in OBS which will update the dropdown list of window names to select from.

## Why I made this
Because I needed to follow some windows while using the newest version of OBS.

Tested versions of OBS: 30.2.2
