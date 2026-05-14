import os
import subprocess
from datetime import datetime

# Windows Start Menu locations
START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
]

# ----------------------
# SEARCH INSTALLED APPS
# ----------------------
def find_app_in_start_menu(app_name):
    app_name = app_name.lower()

    for base_path in START_MENU_PATHS:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith(".lnk"):
                    clean_name = file.lower().replace(".lnk", "")
                    if app_name in clean_name:
                        return os.path.join(root, file)
    return None


# ----------------------
# SPECIAL SYSTEM APPS
# ----------------------
SPECIAL_APPS = {
    "camera": "start microsoft.windows.camera:",
    "settings": "start ms-settings:",
    "photos": "start ms-photos:",
    "voice recorder": "start ms-voice-recorder:",
    "store": "start ms-windows-store:",
    "file explorer": "start explorer:",
    "lock screen": "rundll32.exe user32.dll,LockWorkStation"
}

SPECIAL_CLOSE_APPS = {
    "settings": "SystemSettings.exe",
    "photos": "Microsoft.Photos.exe",
    "camera": "WindowsCamera.exe",
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe"
}

# ----------------------
# SYSTEM ACTIONS
# ----------------------
SYSTEM_ACTIONS = {
    "shutdown": "shutdown /s /t 0",
    "restart": "shutdown /r /t 0",
    "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
}


# ----------------------
# EXECUTE COMMAND
# ----------------------
def execute(command):

    command = command.lower().strip()

    # ---------------- OPEN ----------------
    if command.startswith("open "):
        app = command.replace("open", "", 1).strip()

        # Special apps
        if app in SPECIAL_APPS:
            subprocess.Popen(SPECIAL_APPS[app], shell=True)
            return f"Opening {app}."

        # Search Start Menu
        app_path = find_app_in_start_menu(app)

        if app_path:
            subprocess.Popen(f'start "" "{app_path}"', shell=True)
            return f"Opening {app}."

        # Fallback
        try:
            subprocess.Popen(app, shell=True)
            return f"Opening {app}."
        except:
            return f"I could not find {app} installed on this system."

    # ---------------- CLOSE ----------------
    if command.startswith("close "):

       app = command.replace("close", "", 1).strip()

       if app in SPECIAL_CLOSE_APPS:
          exe_name = SPECIAL_CLOSE_APPS[app]
       else:
          exe_name = app.replace(" ", "") + ".exe"

       subprocess.call(
            f'taskkill /f /im "{exe_name}"',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
        )

       return f"Closing {app}."

    # ---------------- SYSTEM POWER ----------------
    for action in SYSTEM_ACTIONS:
        if action in command:
            subprocess.Popen(SYSTEM_ACTIONS[action], shell=True)
            return f"Executing {action} command."

    # ---------------- BRIGHTNESS ----------------
    if "increase brightness" in command:
        subprocess.call(
            "powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)",
            shell=True
        )
        return "Brightness increased."

    if "decrease brightness" in command:
        subprocess.call(
            "powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,30)",
            shell=True
        )
        return "Brightness decreased."

    # ---------------- TIME ----------------
    if "time" in command:
        now = datetime.now().strftime("%H:%M")
        return f"The current time is {now}."

    return None