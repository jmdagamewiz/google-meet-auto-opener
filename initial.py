
# run this once when using the app
# so the scheduler is run in the background
# everytime your pc turns on

import sys
import os
import winshell
import win32com.client

pythonw_path = sys.executable.replace("python", "pythonw")
schedule_path = os.path.abspath("schedule.py")

# get path of startup folder
startup_folder = winshell.startup()

# creates shortcut file for schedule.py and stores in startup folder
shortcut_path = os.path.join(startup_folder, 'Schedule.lnk')
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = pythonw_path
shortcut.Arguments = schedule_path
shortcut.save()
