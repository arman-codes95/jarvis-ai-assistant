from browser_control import (
    search_google,
    open_first_result,
    open_nth_result,
    go_back,
    close_browser,
    scroll_down,
    scroll_up,
    play_youtube_video,
    play_nth_youtube,
    toggle_play_pause,
    fullscreen_video,
    increase_volume,
    decrease_volume,
    skip_ads,
    refresh_page
)

from system_control import execute
from desktop_tools import copy_text, paste_text, save_file, find_word, replace_word
from dev_tools import save_code_file, run_python_file, run_java_file, open_terminal


def run_tool(tool_name, argument=None):

    # ---------------------- BROWSER ----------------------
   
    if tool_name == "refresh_page":
        if refresh_page():
           return "Refreshing the page."
        return "No browser session active."
    
    if tool_name == "search_google":
        if search_google(argument):
            return f"Searching Google for {argument}."
        return "Search failed."

    if tool_name == "play_youtube":
        if play_youtube_video(argument):
            return f"Playing {argument} on YouTube."
        return "Unable to play the requested video."

    if tool_name == "play_nth_youtube":
        if play_nth_youtube(int(argument)):
            return f"Playing result number {argument}."
        return "No previous YouTube search results."

    if tool_name == "pause_video":
        if toggle_play_pause():
            return "Toggling play or pause."
        return "No active YouTube video."

    if tool_name == "fullscreen_video":
        if fullscreen_video():
            return "Switching fullscreen mode."
        return "No active YouTube video."

    if tool_name == "volume_up":
        if increase_volume():
            return "Increasing volume."
        return "No active YouTube video."

    if tool_name == "volume_down":
        if decrease_volume():
            return "Decreasing volume."
        return "No active YouTube video."

    if tool_name == "skip_ads":
        skip_ads()
        return "Skipping ads if available."

    if tool_name == "open_first_result":
        if open_first_result():
            return "Opening the first result."
        return "Unable to open first result."

    if tool_name == "open_nth_result":
        if open_nth_result(int(argument)):
            return f"Opening result number {argument}."
        return "Unable to open that result."

    if tool_name == "go_back":
        if go_back():
            return "Going back."
        return "No browser session active."

    if tool_name == "scroll_down":
        if scroll_down():
            return "Scrolling down."
        return "No browser session active."

    if tool_name == "scroll_up":
        if scroll_up():
            return "Scrolling up."
        return "No browser session active."

    if tool_name == "close_browser":
        if close_browser():
            return "Closing the browser."
        return "No browser session active."

    # ---------------------- SYSTEM ----------------------

    if tool_name == "system_execute":
        return execute(argument)

    # ---------------------- DESKTOP ----------------------

    if tool_name == "copy_text":
        return copy_text()

    if tool_name == "paste_text":
        return paste_text(argument)

    if tool_name == "save_file":
        return save_file()

    if tool_name == "find_word":
        return find_word(argument)

    if tool_name == "replace_word":
        if isinstance(argument, dict):
            return replace_word(argument.get("old"), argument.get("new"))
        return "Invalid replace arguments."

    # ---------------------- DEV TOOLS ----------------------

    if tool_name == "run_python_file":
        return run_python_file(argument)

    if tool_name == "run_java_file":
        return run_java_file(argument)

    if tool_name == "open_terminal":
        return open_terminal()

    if tool_name == "save_code_file":
        if not isinstance(argument, dict):
            return "Invalid file data provided."

        filename = argument.get("filename")
        content = argument.get("content")

        if not filename or not content:
            return "Filename or content missing."

        return save_code_file(filename, content)

    return "Tool execution failed."