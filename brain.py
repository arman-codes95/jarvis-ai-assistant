from llm_brain import ask_llm
from tools import run_tool
from system_control import execute
from internet import is_connected
import json


def process(command):

    command = command.lower().strip()

    # -------------------
    # 1️⃣ LOCAL SYSTEM COMMANDS
    # -------------------
    result = execute(command)
    if result:
        return result

    # -------------------
    # 2️⃣ DETERMINISTIC TOOL ACTIONS
    # -------------------
    if "search on youtube for" in command:
        query = command.replace("search on youtube for", "").strip()
        if query:
           return run_tool("play_youtube", query)
    # 🔎 Search Google
    if command.startswith("search "):
        query = command.replace("search", "", 1).strip()
        if query:
            return run_tool("search_google", query)
        return "What would you like me to search for?"

    # 🎬 Play first YouTube result from memory
    if "play first" in command:
        return run_tool("play_nth_youtube", 1)

    if "play second" in command:
        return run_tool("play_nth_youtube", 2)
    
    #refresh page
    if "refresh" in command:
        return run_tool("refresh_page")
    
    # 🎥 Play YouTube by query
    if command.startswith("play "):
        query = command.replace("play", "", 1).strip()
        if query:
            return run_tool("play_youtube", query)
        return "What would you like me to play?"

    # ⏯ Pause / Resume
    if "pause" in command or "play" in command:
        return run_tool("pause_video")

    # 🖥 Fullscreen
    if "fullscreen" in command:
        return run_tool("fullscreen_video")

    # 🔊 Volume control
# 🔊 Volume control (flexible)
    if "volume" in command and "increase" in command:
        return run_tool("volume_up")

    if "volume" in command and "decrease" in command:
        return run_tool("volume_down")

    # ⏭ Skip ads
    if "skip ad" in command:
        return run_tool("skip_ads")

    # ⌨ Type text
    if command.startswith("type "):
        text = command.replace("type", "", 1).strip()
        if text:
            return run_tool("type_text", text)
        return "What would you like me to type?"

    # 🌐 Browser navigation
    if command == "open first link":
        return run_tool("open_first_result")

    if command.startswith("open result "):
        parts = command.split()
        if parts[-1].isdigit():
            return run_tool("open_nth_result", parts[-1])
        return "Please specify a valid result number."

    if command == "go back":
        return run_tool("go_back")

    if command in ["close browser", "close chrome"]:
        return run_tool("close_browser")

    # -------------------
    # 3️⃣ INTERNET CHECK BEFORE LLM
    # -------------------
    if not is_connected():
        return "Internet connectivity appears to be offline."
    
    
    # -------------------
    # 4️⃣ LLM INTELLIGENCE SECTION
    # -------------------
    llm_reply = ask_llm(command)

    try:
        data = json.loads(llm_reply)

        if isinstance(data, dict) and "action" in data:
            return run_tool(
                data["action"],
                data.get("argument")
            )

    except json.JSONDecodeError:
        pass

    return llm_reply