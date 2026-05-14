import pyautogui
import pyperclip
import time

# COPY SELECTED TEXT
def copy_text():
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)
    return pyperclip.paste()

# PASTE TEXT
def paste_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    return "Text pasted."

# SAVE FILE
def save_file():
    pyautogui.hotkey("ctrl", "s")
    return "File saved."

# FIND WORD
def find_word(word):
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.5)
    pyperclip.copy(word)
    pyautogui.hotkey("ctrl", "v")
    return f"Searching for {word}."

# REPLACE WORD
def replace_word(old, new):
    pyautogui.hotkey("ctrl", "h")
    time.sleep(0.5)
    pyperclip.copy(old)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("tab")
    pyperclip.copy(new)
    pyautogui.hotkey("ctrl", "v")
    return f"Replacing {old} with {new}."